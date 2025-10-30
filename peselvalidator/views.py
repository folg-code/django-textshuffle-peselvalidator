from django.shortcuts import render

from peselvalidator.forms import PESELForm


def dashboard(request):
    result = None

    if request.method == 'POST':
        form = PESELForm(request.POST)
        if form.is_valid():
            result = {
                'is_valid': True,
                'birth_date': form.cleaned_data['birth_date'],
                'gender': form.cleaned_data['gender']
            }
        else:
            result = {'is_valid': False, 'error': form.errors['pesel'][0]}
    else:
        form = PESELForm()

    return render(request, 'peselvalidator/dashboard.html', {
        'form': form,
        'result': result
    })
