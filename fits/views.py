from django.shortcuts import render, redirect, get_object_or_404
from .models import Closet, Fit
from .forms import ClosetForm, FitForm
from django.http import Http404
from django.db.models import Q


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


def fit(request, owner, shown_id):
    fit = Fit.objects.get(shown_id=shown_id, owner__username=owner)
    context = {
        'fit': fit
    }
    return render(request, 'fits/fit.html', context)


def new_closet(request, owner):
    """Create new closet"""
    if owner != str(request.user):
        raise Http404
    if request.method != 'POST':
        form = ClosetForm()
    else:
        form = ClosetForm(data=request.POST)
        if form.is_valid():
            new_closet = form.save(commit=False)
            new_closet.owner = request.user
            new_closet.save()
            return redirect('fits:closets', owner=new_closet.owner)

    context = {'form': form,
               'owner': owner}
    return render(request, 'fits/new_closet.html', context)


def new_fit(request, owner):
    """Create new Outfit"""
    if owner != str(request.user):
        raise Http404

    if request.method != 'POST':
        form = FitForm()
    else:
        form = FitForm(request.POST, request.FILES)

        if form.is_valid():
            new_fit = form.save(commit=False)
            main_closet = Closet.objects.get(style__exact="main_closet")
            main_closet.save()
            new_fit.owner = request.user
            new_fit.save()
            products = request.POST.getlist('closet')
            for product in products:
                if Closet.objects.all().exists():
                    product = Closet.objects.get(pk=product)
                    new_fit.closet.add(product)
            new_fit.closet.add(main_closet)
            return redirect('fits:closets', owner=new_fit.owner)

    context = {'form': form,
               'owner': owner}
    return render(request, 'fits/new_fit.html', context)


def delete_fit(request, shown_id, owner):
    fit = get_object_or_404(Fit, shown_id=shown_id, owner__username=owner)
    if request.method == "POST":
        fit.delete()
        return redirect('fits:closets', owner=fit.owner)
    context = {'fit': fit}
    return render(request, "fits/delete_fit.html", context)


def edit_fit(request, shown_id, owner):
    fit = get_object_or_404(Fit, shown_id=shown_id, owner__username=owner)
    if request.method != 'POST':
        form = FitForm(instance=fit)
    else:
        form = FitForm(request.POST, request.FILES, instance=fit)
        if form.is_valid():
            form.save()
            return redirect('fits:closets', owner=fit.owner)
    context = {'fit': fit, 'form': form}
    return render(request, 'fits/edit_fit.html', context)


def delete_closet(request, owner, style):
    closet = get_object_or_404(Closet, ~Q(style='main_closet'), owner__username=owner, style=style)
    if request.method == "POST":
        closet.delete()
        return redirect('fits:closets', owner=closet.owner)
    context = {'closet': closet}
    return render(request, "fits/delete_closet.html", context)


def remove_fit(request, owner, style, fit_shown_id):
    closet = get_object_or_404(Closet, ~Q(style='main_closet'), owner__username=owner, style=style)
    fit = get_object_or_404(Fit, owner__username=owner, shown_id=fit_shown_id)
    closet.fit_set.remove(fit)
    context = {
        'closet': closet,
        'fit': fit
    }
    return render(request, "fits/single_closet.html", context)


def remove_fits(request, style, owner):
    closet = get_object_or_404(Closet, ~Q(style='main_closet'), owner__username=owner, style=style)
    fits = closet.fit_set.order_by('-date_added')
    if request.GET.get('DeleteButton'):
        closet.fit_set.remove(request.GET.get('DeleteButton'))

    context = {
        'closet': closet,
        'fits': fits
    }
    return render(request, 'fits/remove_fits.html', context)


def add_fits(request, owner, style):
    curr_closet = get_object_or_404(Closet, ~Q(style='main_closet'), style=style, owner__username=owner)
    main_closet = Closet.objects.get(style='main_closet', owner__username=owner)
    curr_fits = curr_closet.fit_set.all()
    main_fits = main_closet.fit_set.all()
    fits = main_fits.difference(curr_fits).order_by('-date_added')
    if request.GET.get('AddButton'):
        curr_closet.fit_set.add(request.GET.get('AddButton'))
        return redirect('fits:add_fits', owner=curr_closet.owner, style=curr_closet.style)

    context = {
        'main_closet': main_closet,
        'curr_closet': curr_closet,
        'fits': fits
    }
    return render(request, 'fits/add_fits.html', context)



