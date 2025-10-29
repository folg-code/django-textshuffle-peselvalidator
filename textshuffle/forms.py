from django import forms


class UploadTextForm(forms.Form):
    file = forms.FileField(label="Wgraj plik tekstowy")

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        try:
            content = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            raise forms.ValidationError(
                "Nieprawidłowy format pliku. Proszę wgrać plik tekstowy "
            )
        self.cleaned_data['text_content'] = content
        return uploaded_file
