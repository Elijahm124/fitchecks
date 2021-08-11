from django.shortcuts import render
from .models import Closet


def index(request):
    return render(request, 'fits/index.html')


def closet(request, style, owner):
    closet = Closet.objects.get(style=style, owner__username=owner)
    fits = closet.fit_set.order_by('-date_added')
    context = {
        'closet': closet,
        'fits': fits
    }
    return render(request, 'fits/closet.html', context)


def fit(request, style, owner, fit_id):
    closet = Closet.objects.get(style=style, owner__username=owner)
    fit = closet.fit_set.get(closet__fit__id=fit_id)
    context = {
        'closet': closet,
        'fit': fit
    }
    return render(request, 'fits/fit.html', context)
