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
