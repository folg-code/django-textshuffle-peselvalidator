import random
import re

from django.shortcuts import render

from textshuffle.forms import UploadTextForm


def dashboard(request):
    text_to_display = ""
    is_shuffled = False
    header = ""

    if request.method == 'POST':
        if 'upload' in request.POST:
            form = UploadTextForm(request.POST, request.FILES)
            if form.is_valid():
                text_to_display = form.cleaned_data['text_content']
                header = "Oryginalny tekst"
        elif 'shuffle' in request.POST:
            form = UploadTextForm()
            text_to_display = request.POST.get('text_to_display', '')
            if text_to_display:
                text_to_display = shuffle_text(text_to_display)
                is_shuffled = True
                header = "Zamieszany tekst"
    else:
        form = UploadTextForm()

    return render(request, 'textshuffle/dashboard.html', {
        'text_to_display': text_to_display,
        'is_shuffled': is_shuffled,
        'header': header,
        'form': form
    })

def shuffle_text(text):
    def shuffle_word(word):
        if len(word) <= 3:
            return word
        middle = list(word[1:-1])
        random.shuffle(middle)
        return word[0] + "".join(middle) + word[-1]

    return re.sub(r'\w+', lambda m: shuffle_word(m.group()), text)
