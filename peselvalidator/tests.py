from datetime import date

from django.test import TestCase, Client

from peselvalidator.forms import PESELForm
from peselvalidator.utils import parse_pesel, InvalidPESEL


class PESELFormTest(TestCase):

    def test_valid_pesel(self):
        form = PESELForm(data={"pesel": "44051401458"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['birth_date'], date(1944, 5, 14))
        self.assertEqual(form.cleaned_data['gender'], "Mężczyzna")

    def test_invalid_pesel(self):
        form = PESELForm(data={"pesel": "4405140A458"})
        self.assertFalse(form.is_valid())
        self.assertIn("PESEL może zawierać tylko cyfry", form.errors['pesel'][0])


class ParsePESELTest(TestCase):

    def test_valid_pesel(self):
        result = parse_pesel("44051401458")
        self.assertEqual(result['birth_date'], date(1944, 5, 14))
        self.assertEqual(result['gender'], "Mężczyzna")

    def test_invalid_characters(self):
        with self.assertRaises(InvalidPESEL) as cm:
            parse_pesel("4405140A458")
        self.assertIn("PESEL może zawierać tylko cyfry", str(cm.exception))

    def test_invalid_length(self):
        with self.assertRaises(InvalidPESEL) as cm:
            parse_pesel("1234567890")
        self.assertIn("PESEL powinien mieć dokładnie 11 cyfr", str(cm.exception))

    def test_wrong_checksum(self):
        with self.assertRaises(InvalidPESEL) as cm:
            parse_pesel("44051401459")
        self.assertIn("Niepoprawna cyfra kontrolna PESEL", str(cm.exception))

    def test_invalid_date(self):
        with self.assertRaises(InvalidPESEL) as cm:
            parse_pesel("44053201458")
        self.assertIn("Niepoprawna data urodzenia w numerze PESEL", str(cm.exception))


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
