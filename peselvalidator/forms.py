from datetime import date

from django import forms

from peselvalidator.utils import parse_pesel, InvalidPESEL


class PESELForm(forms.Form):
    pesel = forms.CharField(
        label="Numer PESEL",
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={'placeholder': 'Wprowadź PESEL'})
    )

    def clean_pesel(self):
        pesel = self.cleaned_data['pesel']

        try:
            result = parse_pesel(pesel)
        except InvalidPESEL as e:
            raise forms.ValidationError(str(e))

        # dodajemy dane zwrócone przez logikę domenową
        self.cleaned_data.update(result)
        return pesel
