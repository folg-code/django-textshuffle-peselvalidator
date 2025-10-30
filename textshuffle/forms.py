from django import forms


class UploadTextForm(forms.Form):
    file = forms.FileField(label="Wgraj plik tekstowy")

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')

        try:
            content = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            raise forms.ValidationError(
                "Nieprawidłowy format pliku. Proszę wgrać plik tekstowy w kodowaniu UTF-8."
            )
        except Exception as e:
            raise forms.ValidationError(
                f"Wystąpił nieoczekiwany błąd podczas przetwarzania pliku: {str(e)}"
            )

        if not content.strip():
            raise forms.ValidationError("Plik jest pusty lub nie zawiera tekstu.")

        self.cleaned_data['text_content'] = content
        return uploaded_file
