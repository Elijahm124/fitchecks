from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        raise Http404

    if request.method != 'POST':
        # blank registration form
        uform = UserCreationForm()
        pform = ProfileForm()
    else:
        pform = ProfileForm(request.POST, request.FILES)
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


@login_required
def edit_profile(request, owner):
    if owner != str(request.user):
        raise Http404

    profile = get_object_or_404(Profile, user__username=owner)
    if request.method != 'POST':
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('fits:closets', owner=owner)
    context = {'profile': profile, 'form': form}
    return render(request, 'registration/edit_profile.html', context)


@login_required
def delete_profile(request, owner):
    if owner != str(request.user):
        raise Http404

    user = request.user
    if request.method == "POST":
        user.delete()
        return redirect('fits:all')
    context = {'user': user}
    return render(request, "registration/delete_profile.html", context)



