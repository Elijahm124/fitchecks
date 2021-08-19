from django.shortcuts import render, redirect, get_object_or_404
from .models import Closet, Fit
from users.models import Profile
from .forms import ClosetForm, FitForm
from django.contrib.auth.models import User
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'fits/index.html')


def closets(request, owner):
    closets = Closet.objects.filter(owner__username=owner).order_by('-date_added')
    context = {}
    same = True
    if owner != str(request.user) and request.user.is_authenticated:
        print("not same")
        same = False
        curr_user = request.user.profile
        followee = Profile.objects.get(user__username=owner)
        follower = followee.followers.all()
        if curr_user not in follower:
            is_following = False
            if request.method == "POST":
                print("follow")
                curr_user.following.add(followee)
                followee.followers.add(curr_user)
                is_following = True
        else:
            is_following = True
            if request.method == "POST":
                print("unfollowed")
                curr_user.following.remove(followee)
                followee.followers.remove(curr_user)
                is_following = False
        context.update({'curr_user': curr_user,
                        'followee': followee,
                        'is_following': is_following})
    owner = get_object_or_404(User, username=owner)
    context.update({'closets': closets,
                    'owner': owner,
                    'same': same})

    return render(request, "fits/closets.html", context)


def closet(request, style, owner):
    closet = Closet.objects.get(style=style, owner__username=owner)
    same = True
    if owner != str(request.user):
        same = False
    owner = get_object_or_404(User, username=owner)
    fits = closet.fit_set.order_by('-date_added')
    context = {
        'closet': closet,
        'fits': fits,
        'owner': owner,
        'same': same
    }
    return render(request, 'fits/single_closet.html', context)


def fit(request, owner, shown_id):
    fit = Fit.objects.get(shown_id=shown_id, owner__username=owner)
    same = True
    if owner != str(request.user):
        same = False
    owner = get_object_or_404(User, username=owner)
    context = {
        'fit': fit,
        'owner': owner,
        'same': same,
    }
    return render(request, 'fits/fit.html', context)


@login_required
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


@login_required
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
            main_closet = Closet.objects.get(style__exact="main_closet", owner__username=owner)
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


@login_required
def delete_fit(request, shown_id, owner):
    if owner != str(request.user):
        raise Http404
    fit = get_object_or_404(Fit, shown_id=shown_id, owner__username=owner)
    if request.method == "POST":
        fit.delete()
        return redirect('fits:closets', owner=fit.owner)
    context = {'fit': fit}
    return render(request, "fits/delete_fit.html", context)


@login_required
def edit_fit(request, shown_id, owner):
    if owner != str(request.user):
        raise Http404
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


@login_required
def delete_closet(request, owner, style):
    if owner != str(request.user):
        raise Http404
    closet = get_object_or_404(Closet, ~Q(style='main_closet'), owner__username=owner, style=style)
    if request.method == "POST":
        closet.delete()
        return redirect('fits:closets', owner=closet.owner)
    context = {'closet': closet}
    return render(request, "fits/delete_closet.html", context)


@login_required
def remove_fits(request, style, owner):
    if owner != str(request.user):
        raise Http404
    closet = get_object_or_404(Closet, ~Q(style='main_closet'), owner__username=owner, style=style)
    fits = closet.fit_set.order_by('-date_added')
    if request.GET.get('DeleteButton'):
        closet.fit_set.remove(request.GET.get('DeleteButton'))

    context = {
        'closet': closet,
        'fits': fits
    }
    return render(request, 'fits/remove_fits.html', context)


@login_required
def add_fits(request, owner, style):
    if owner != str(request.user):
        raise Http404
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


