from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ProfileForm


def register(request):
    if request.method != 'POST':
        # blank registration form
        form = ProfileForm()
    else:
        form = ProfileForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()

            login(request, new_user)
            return redirect('fits:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)
