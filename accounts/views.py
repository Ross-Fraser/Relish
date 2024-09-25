from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password1 = form.cleaned_data.get('password1')
            raw_password2 = form.cleaned_data.get('password2')
            if raw_password1 != raw_password2:
                form.add_error('password2',
                               'The two password fields didn’t match.')
            else:
                form.save()
                user = authenticate(username=username, password=raw_password1)
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
