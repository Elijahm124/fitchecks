from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method != 'POST':
        # blank registration form
        uform = UserCreationForm()
        pform = ProfileForm()
    else:
        pform = ProfileForm(data=request.POST)
        uform = UserCreationForm(data=request.POST)

        if uform.is_valid() and pform.is_valid():
            new_user = uform.save()
            new_profile = pform.save(commit=False)
            new_profile.user = new_user
            new_profile.save()

            login(request, new_user)
            return redirect('fits:index')

    context = {'uform': uform,
               'pform': pform}
    return render(request, 'registration/register.html', context)
