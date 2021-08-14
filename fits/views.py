from django.shortcuts import render, redirect
from .models import Closet, Fit
from .forms import NewClosetForm, NewFitForm
from django.http import Http404


def index(request):
    return render(request, 'fits/index.html')


def closets(request, owner):
    closets = Closet.objects.filter(owner__username=owner).order_by('-date_added')
    context = {'closets': closets,
               'owner': owner}
    return render(request, "fits/closets.html", context)


def closet(request, style, owner):
    closet = Closet.objects.get(style=style, owner__username=owner)
    fits = closet.fit_set.order_by('-date_added')
    context = {
        'closet': closet,
        'fits': fits
    }
    return render(request, 'fits/single_closet.html', context)


def fit(request, owner, fit_id):
    fit = Fit.objects.get(closet__fit__id=fit_id, owner__username=owner)
    context = {
        'fit': fit
    }
    return render(request, 'fits/fit.html', context)


def new_closet(request, owner):
    """Create new closet"""
    if owner != str(request.user):
        raise Http404
    if request.method != 'POST':
        form = NewClosetForm()
    else:
        form = NewClosetForm(data=request.POST)
        if form.is_valid():
            new_closet = form.save(commit=False)
            new_closet.owner = request.user
            new_closet.save()
            return redirect('fits:closets')

    context = {'form': form,
               'owner': owner}
    return render(request, 'fits/new_closet.html', context)


def new_fit(request, owner):
    """Create new Outfit"""
    if owner != str(request.user):
        raise Http404

    if request.method != 'POST':
        form = NewFitForm()
    else:
        form = NewFitForm(request.POST, request.FILES)
        if form.is_valid():
            new_fit = form.save(commit=False)
            new_fit.owner = request.user
            new_fit.save()
            return redirect('fits:single_closet', owner=new_fit.owner, style=new_fit.closet.style)

    context = {'form': form,
               'owner': owner}
    return render(request, 'fits/new_fit.html', context)
