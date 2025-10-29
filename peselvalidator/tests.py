from datetime import date

from django.test import TestCase, Client

from peselvalidator.forms import PESELForm


class PESELFormTest(TestCase):

    def test_valid_pesel(self):
        pesel = '44051401458'  # poprawny PESEL
        form = PESELForm(data={'pesel': pesel})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['birth_date'], date(1944, 5, 14))
        self.assertEqual(form.cleaned_data['gender'], 'Mężczyzna')

    def test_invalid_characters(self):
        form = PESELForm(
            data={'pesel': '4405140A458'}
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "PESEL może zawierać tylko cyfry",
            form.errors['pesel'][0]
        )

    def test_invalid_length(self):
        form = PESELForm(
            data={'pesel': '1234567890'}
        )
        self.assertFalse(form.is_valid())

    def test_wrong_checksum(self):
        form = PESELForm(
            data={'pesel': '44051401459'}
        )  # ostatnia cyfra zmieniona
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Niepoprawna cyfra kontrolna PESEL",
            form.errors['pesel'][0]
        )

    def test_invalid_date(self):
        form = PESELForm(data={'pesel': '44053201458'})
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Niepoprawna data urodzenia w numerze PESEL",
            form.errors['pesel'][0]
        )


class PESELViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_dashboard_get(self):
        response = self.client.get('/peselvalidator/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Numer PESEL')

    def test_dashboard_post_valid(self):
        response = self.client.post(
            '/peselvalidator/', {'pesel': '44051401458'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mężczyzna')
        self.assertContains(response, '14 maja 1944')

    def test_dashboard_post_invalid(self):
        response = self.client.post(
            '/peselvalidator/', {'pesel': '12345678901'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Niepoprawna')
