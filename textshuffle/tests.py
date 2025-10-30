from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from textshuffle.forms import UploadTextForm
from textshuffle.utils import shuffle_text


class ShuffleTextUtilsTest(TestCase):
    def test_short_words_remain_same(self):
        text = "To ja my"
        result = shuffle_text(text)
        self.assertEqual(result, text)

    def test_long_word_shuffled(self):
        word = "przyklad"
        shuffled = shuffle_text(word)
        self.assertEqual(shuffled[0], word[0])
        self.assertEqual(shuffled[-1], word[-1])
        self.assertCountEqual(shuffled[1:-1], word[1:-1])

    def test_text_with_punctuation(self):
        text = "Hello, world!"
        result = shuffle_text(text)
        self.assertTrue(result[0] == 'H')
        self.assertTrue(result[-1] == '!')


class UploadTextFormTest(TestCase):
    def test_valid_file(self):
        content = b"To jest test"
        uploaded_file = SimpleUploadedFile("test.txt", content)
        form = UploadTextForm(files={'file': uploaded_file})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['text_content'], "To jest test")

    def test_invalid_file_encoding(self):
        content = b"\xff\xfe\x00\x00"
        uploaded_file = SimpleUploadedFile("bad.txt", content)
        form = UploadTextForm(files={'file': uploaded_file})
        self.assertFalse(form.is_valid())
        self.assertIn("Nieprawidłowy format pliku", str(form.errors))


class TextShuffleViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard_get(self):
        response = self.client.get('/textshuffle/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wgraj plik')

    def test_dashboard_post_valid(self):
        content = b"Testowy tekst"
        uploaded_file = SimpleUploadedFile("test.txt", content)
        response = self.client.post('/textshuffle/', {'file': uploaded_file})
        # Powinien przekierować do widoku 'result'
        self.assertEqual(response.status_code, 302)

    def test_dashboard_post_invalid_file(self):
        content = b"\xff\xfe"
        uploaded_file = SimpleUploadedFile("bad.txt", content)
        response = self.client.post('/textshuffle/', {'file': uploaded_file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nieprawidłowy format pliku")

    def test_result_redirect_if_no_session(self):
        response = self.client.get('/textshuffle/result/')
        # jeśli brak sesji, powinno przekierować do dashboard
        self.assertEqual(response.status_code, 302)

    def test_result_display_shuffled_text(self):
        session = self.client.session
        session['text_to_shuffle'] = "Testowy tekst"
        session.save()

        response = self.client.get('/textshuffle/result/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testowy")
