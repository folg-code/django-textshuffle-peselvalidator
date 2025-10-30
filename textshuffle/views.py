
from django.shortcuts import render, redirect

from textshuffle.forms import UploadTextForm
from textshuffle.utils import shuffle_text


def dashboard(request):
    form = UploadTextForm()
    error_message = ""

    if request.method == 'POST':
        form = UploadTextForm(request.POST, request.FILES)
        if form.is_valid():
            text_content = form.cleaned_data['text_content']
            text_content_shuffled = shuffle_text(text_content)
            request.session['text_to_shuffle'] = text_content_shuffled
            return redirect('textshuffle:result')
        else:
            error_message = form.errors.get('file', ["Nieprawidłowy plik"])[0]

    return render(request, 'textshuffle/dashboard.html', {
        'form': form,
        'error_message': error_message
    })


def result(request):
    text_to_shuffle = request.session.get('text_to_shuffle', '')

    if not text_to_shuffle:
        return redirect('textshuffle:dashboard')

    # Zamieszaj ponownie jeśli kliknięto przycisk
    if request.method == 'POST' and 'shuffle' in request.POST:
        text_to_shuffle = shuffle_text(text_to_shuffle)
        request.session['text_to_shuffle'] = text_to_shuffle

    return render(request, 'textshuffle/result.html', {
        'shuffled_text': text_to_shuffle
    })
