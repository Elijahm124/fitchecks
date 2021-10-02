from django.shortcuts import render, redirect, get_object_or_404
from .models import Closet, Fit, Top, Accessory, Bottom, Shoe, Like
from users.models import Profile
from .forms import ClosetForm, FitForm, TopForm, AccessoryForm, ShoeForm, BottomForm, AccessoryFormSet, CommentForm, \
    LikedFitsForm
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    if request.user.is_authenticated:
        return redirect("fits:feed")

    return render(request, 'fits/index.html')


def feed(request):
    context = {}
    following = []
    followed_people = request.user.profile.following.all()
    fits = Fit.objects.filter(owner__profile__in=followed_people, private=False) | \
           Fit.objects.filter(owner__username=request.user).order_by("-date_added")

    context.update({'fits': fits})

    if not request.user.is_authenticated:
        return redirect("fits:all")

    else:
        liked = [i for i in Fit.objects.all() if Like.objects.filter(user=request.user, fit=i)]
        context['liked_post'] = liked
        for fit in fits:
            curr_user = request.user.profile
            followee = Profile.objects.get(user__username=fit.owner)
            follower = followee.followers.all()
            if curr_user in follower:
                following.append(fit)
    context["following_user"] = following

    page = request.GET.get('page', 1)
    paginator = Paginator(fits, 2)
    try:
        fitz = paginator.page(page)
    except PageNotAnInteger:
        fitz = paginator.page(1)
    except EmptyPage:
        fitz = paginator.page(paginator.num_pages)
    context.update({"fitz": fitz})

    return render(request, 'fits/feed.html', context)


def all(request):
    fits = Fit.objects.filter(private=False).order_by("-date_added")
    context = {'fits': fits}
    following = []

    if request.user.is_authenticated:
        liked = [i for i in Fit.objects.all() if Like.objects.filter(user=request.user, fit=i)]
        context['liked_post'] = liked

        for fit in fits:
            curr_user = request.user.profile
            followee = Profile.objects.get(user__username=fit.owner)
            follower = followee.followers.all()
            if curr_user in follower:
                following.append(fit)
    context["following_user"] = following

    page = request.GET.get('page', 1)
    paginator = Paginator(fits, 2)
    try:
        fitz = paginator.page(page)
    except PageNotAnInteger:
        fitz = paginator.page(1)
    except EmptyPage:
        fitz = paginator.page(paginator.num_pages)
    context.update({"fitz": fitz})

    return render(request, 'fits/all.html', context)


def closets(request, owner):
    if owner == str(request.user):
        closets = Closet.objects.filter(owner__username=owner).order_by('-date_added')
        same = True
    else:
        closets = Closet.objects.filter(owner__username=owner, private=False).order_by('-date_added')
    context = {}
    is_following = False

    if request.user.is_authenticated:
        if owner != str(request.user):
            same = False
        curr_user = request.user.profile
        followee = Profile.objects.get(user__username=owner)
        follower = followee.followers.all()
        if curr_user in follower:
            is_following = True

    owner = get_object_or_404(User, username=owner)
    context.update({'closets': closets,
                    'owner': owner,
                    "is_following": is_following,
                    "same": same}
                   )

    return render(request, "fits/closets.html", context)


def closet(request, style, owner):
    closet = Closet.objects.get(style=style, owner__username=owner)
    if closet.style == "liked_fits":
        return redirect("fits:liked_fits", owner)
    same = True
    if owner == str(request.user):
        fits = closet.fit_set.order_by('-date_added')
    else:
        if closet.private:
            raise Http404
        same = False
        fits = closet.fit_set.filter(private=False).order_by('-date_added')

    owner = get_object_or_404(User, username=owner)

    context = {
        'closet': closet,
        'fits': fits,
        'owner': owner,
        'same': same
    }
    return render(request, 'fits/single_closet.html', context)


def fit(request, owner, shown_id):
    context = {}
    fit = Fit.objects.get(shown_id=shown_id, owner__username=owner)
    if request.user.is_authenticated:
        liked = [i for i in Fit.objects.all() if Like.objects.filter(user=request.user, fit=i)]
        context['liked_post'] = liked

    try:
        bottom = fit.bottom_set.all()[0]
    except IndexError:
        pass
    else:
        context.update({"bottom": bottom})

    try:
        shoe = fit.shoe_set.all()[0]
    except IndexError:
        pass
    else:
        context.update({"shoe": shoe})

    same = True
    if owner != str(request.user):
        if fit.private:
            raise Http404
        same = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.fit = fit
            data.username = request.user
            data.save()
            return redirect('fits:fit', owner=fit.owner, shown_id=shown_id)
    else:
        form = CommentForm()

    owner = get_object_or_404(User, username=owner)
    context.update({
        'fit': fit,
        'owner': owner,
        'same': same,
        'form': form,
    })
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

    context = {'owner': owner, }
    if request.method != 'POST':
        form = FitForm()
        top_form = TopForm()
        bottom_form = BottomForm()
        accessory_form = AccessoryForm()
        shoe_form = ShoeForm()
        context.update({"form": form,
                        'top_form': top_form,
                        "bottom_form": bottom_form,
                        "accessory_form": accessory_form,
                        'shoe_form': shoe_form})
        request.session['top_count'] = 0
        request.session['shoe_count'] = 0
        request.session['bottom_count'] = 0
        request.session['accessory_count'] = 0

    if request.method == "POST" and "new_top" in request.POST:

        top_form = TopForm(data=request.POST)
        if top_form.is_valid() and request.is_ajax():
            request.session['top_count'] += 1
            request.session[f'top_form_{request.session[f"top_count"]}'] = top_form.cleaned_data

    if request.method == "POST" and "new_bottom" in request.POST:

        bottom_form = BottomForm(data=request.POST)
        if bottom_form.is_valid() and request.is_ajax():
            request.session["bottom_count"] += 1
            request.session['bottom_form'] = bottom_form.cleaned_data

    if request.method == "POST" and "new_shoe" in request.POST:

        shoe_form = ShoeForm(data=request.POST)
        if shoe_form.is_valid() and request.is_ajax():
            request.session["shoe_count"] += 1
            request.session['shoe_form'] = shoe_form.cleaned_data

    if request.method == "POST" and "new_accessory" in request.POST:

        accessory_form = AccessoryForm(data=request.POST)
        if accessory_form.is_valid() and request.is_ajax():
            request.session["accessory_count"] += 1
            request.session[f'accessory_form_{request.session[f"accessory_count"]}'] = accessory_form.cleaned_data

    if request.method == "POST" and "add_fit" in request.POST:

        form = FitForm(request.POST, request.FILES)

        if form.is_valid():
            new_fit = form.save(commit=False)
            main_closet = Closet.objects.get(style__exact="main_closet", owner__username=owner)
            main_closet.save()

            new_fit.owner = request.user
            new_fit.save()

            if request.session['top_count'] > 0:
                for i in range(1, request.session['top_count'] + 1):
                    top = Top.objects.create(**request.session[f'top_form_{i}'])
                    new_fit.top_set.add(top)
            if request.session['bottom_count'] > 0:
                bottom = Bottom.objects.create(**request.session['bottom_form'])
                new_fit.bottom_set.add(bottom)
            if request.session['shoe_count'] > 0:
                shoe = Shoe.objects.create(**request.session['shoe_form'])
                new_fit.shoe_set.add(shoe)
            if request.session['accessory_count'] > 0:
                for i in range(1, request.session['accessory_count'] + 1):
                    accessory = Accessory.objects.create(**request.session[f'accessory_form_{i}'])
                    new_fit.accessory_set.add(accessory)

            products = request.POST.getlist('closet')
            for product in products:
                if Closet.objects.all().exists():
                    product = Closet.objects.get(pk=product)
                    new_fit.closet.add(product)
            new_fit.closet.add(main_closet)

            return redirect('fits:closets', owner=new_fit.owner)

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
    context = {}
    if owner != str(request.user):
        raise Http404
    fit = get_object_or_404(Fit, shown_id=shown_id, owner__username=owner)
    if request.method != 'POST':
        form = FitForm(instance=fit)

    else:
        form = FitForm(request.POST, request.FILES, instance=fit)
        if form.is_valid():
            edited_fit = form.save(commit=False)
            main_closet = Closet.objects.get(style__exact="main_closet", owner__username=owner)
            main_closet.save()
            edited_fit.closet.add(main_closet)
            edited_fit.save()

            return redirect('fits:closets', owner=fit.owner)

    context.update({'fit': fit, 'form': form})
    return render(request, 'fits/edit_fit.html', context)


@login_required
def edit_fit_elements(request, shown_id, owner):
    if owner != str(request.user):
        raise Http404
    fit = get_object_or_404(Fit, shown_id=shown_id, owner__username=owner)
    context = {"fit": fit}

    if request.method == "POST":
        top_form1 = None
        top_form2 = None
        bottom_form = None
        shoe_form = None
        accessory_formset = None
        forms_valid = True

        if len(fit.top_set.all()) == 2:
            top_form1 = TopForm(request.POST, instance=fit.top_set.all()[0])
            top_form2 = TopForm(request.POST, instance=fit.top_set.all()[1])
            context.update({"top_form1": top_form1, "top_form2": top_form2})
        elif len(fit.top_set.all()) == 1:
            top_form1 = TopForm(request.POST, instance=fit.top_set.all()[0])
            context.update({"top_form1": top_form1})
        if len(fit.bottom_set.all()) == 1:
            bottom_form = BottomForm(request.POST, instance=fit.bottom_set.all()[0])
            context.update({"bottom_form": bottom_form})
        if len(fit.shoe_set.all()) == 1:
            shoe_form = ShoeForm(request.POST, instance=fit.shoe_set.all()[0])
            context.update({"shoe_form": shoe_form})
        if len(fit.accessory_set.all()) > 0:
            accessory_formset = AccessoryFormSet(request.POST, queryset=fit.accessory_set.all())
            context.update({"accessory_formset": accessory_formset})

        if top_form1:
            if top_form1.is_valid():
                top_form1.save()
            else:
                forms_valid = False
        if top_form2:
            if top_form2.is_valid():
                top_form2.save()
            else:
                forms_valid = False
        if bottom_form:
            if bottom_form.is_valid():
                bottom_form.save()
            else:
                forms_valid = False
        if shoe_form:
            if shoe_form.is_valid():
                shoe_form.save()
            else:
                forms_valid = False
        if accessory_formset:
            if accessory_formset.is_valid():
                accessory_formset.save()
            else:
                forms_valid = False

        if forms_valid:
            return redirect('fits:fit', owner=fit.owner, shown_id=shown_id)
    elif request.GET.get('DeleteButton'):
        element = None
        if "top" in request.GET:
            element = get_object_or_404(Top, pk=request.GET.get('DeleteButton'))
        elif "bottom" in request.GET:
            element = get_object_or_404(Bottom, pk=request.GET.get('DeleteButton'))
        elif "shoe" in request.GET:
            element = get_object_or_404(Shoe, pk=request.GET.get('DeleteButton'))
        elif "accessory" in request.GET:
            element = get_object_or_404(Accessory, pk=request.GET.get('DeleteButton'))
        element.delete()
        return redirect('fits:edit_fit_elements', owner=fit.owner, shown_id=shown_id)

    else:
        if len(fit.top_set.all()) == 2:
            top_1 = fit.top_set.all()[0]
            top_form1 = TopForm(instance=top_1)

            top_2 = fit.top_set.all()[1]
            top_form2 = TopForm(instance=top_2)
            context.update({"top_form1": top_form1, "top_form2": top_form2, "top_1": top_1, "top2": top_2})
        elif len(fit.top_set.all()) == 1:
            top_1 = fit.top_set.all()[0]
            top_form1 = TopForm(instance=top_1)
            context.update({"top_form1": top_form1, "top_1": top_1})

        if len(fit.bottom_set.all()) == 1:
            bottom = fit.bottom_set.all()[0]
            bottom_form = BottomForm(instance=bottom)
            context.update({"bottom_form": bottom_form, "bottom": bottom})
        if len(fit.shoe_set.all()) == 1:
            shoe = fit.shoe_set.all()[0]
            shoe_form = ShoeForm(instance=shoe)
            context.update({"shoe_form": shoe_form, "shoe": shoe})
        if len(fit.accessory_set.all()) > 0:
            accessories = fit.accessory_set.all()
            accessory_formset = AccessoryFormSet(queryset=accessories)
            context.update({"accessory_formset": accessory_formset, "accessories": accessories})

    return render(request, 'fits/edit_fit_elements.html', context)


@login_required
def edit_closet(request, owner, style):
    if owner != str(request.user):
        raise Http404
    closet = get_object_or_404(Closet, ~Q(style='main_closet'), ~Q(style='liked_fits'), style=style,
                               owner__username=owner)
    if request.method != 'POST':
        form = ClosetForm(instance=closet)
    else:
        form = ClosetForm(request.POST, """request.FILES""", instance=closet)
        if form.is_valid():
            form.save()
            return redirect('fits:single_closet', style=closet.style, owner=closet.owner)
    context = {'closet': closet, 'form': form}
    return render(request, 'fits/edit_closet.html', context)


@login_required
def delete_closet(request, owner, style):
    if owner != str(request.user):
        raise Http404
    closet = get_object_or_404(Closet, ~Q(style='main_closet'), ~Q(style='liked_fits'), owner__username=owner,
                               style=style)
    if request.method == "POST":
        closet.delete()
        return redirect('fits:closets', owner=closet.owner)
    context = {'closet': closet}
    return render(request, "fits/delete_closet.html", context)


@login_required
def remove_fits(request, style, owner):
    if owner != str(request.user):
        raise Http404
    closet = get_object_or_404(Closet, ~Q(style='main_closet'), ~Q(style='liked_fits'), owner__username=owner,
                               style=style)
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
    curr_closet = get_object_or_404(Closet, ~Q(style='main_closet'), ~Q(style='liked_fits'), style=style,
                                    owner__username=owner)
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


@login_required
def add_fit_elements(request, shown_id, owner):
    if owner != str(request.user):
        raise Http404
    fit = get_object_or_404(Fit, shown_id=shown_id, owner__username=owner)
    context = {"fit": fit}

    if request.method != "POST":
        request.session['top_count'] = len(fit.top_set.all())
        request.session['shoe_count'] = len(fit.shoe_set.all())
        request.session['bottom_count'] = len(fit.bottom_set.all())
        request.session['accessory_count'] = len(fit.accessory_set.all())
        context.update({"top_count": request.session['top_count'],
                        "shoe_count": request.session['shoe_count'],
                        "bottom_count": request.session['bottom_count'],
                        "accessory_count": request.session['accessory_count']})
        if request.session['top_count'] < 2:
            top_form = TopForm()
            context.update({
                'top_form': top_form,
            })
        elif request.session['bottom_count'] == 0:
            bottom_form = BottomForm()
            context.update({
                'bottom_form': bottom_form})
        elif request.session['accessory_count'] < 6:
            accessory_form = AccessoryForm()
            context.update({
                'accessory_form': accessory_form})
        elif request.session['shoe_count'] == 0:
            shoe_form = ShoeForm()
            context.update({
                'shoe_form': shoe_form})
        else:
            full_form = True
            context.update({"full_form": full_form})

    else:
        if "new_top" in request.POST:

            top_form = TopForm(data=request.POST)
            if top_form.is_valid() and request.is_ajax():
                top = Top.objects.create(top_form.cleaned_data)
                fit.top_set.add(top)
                request.session['top_count'] += 1

        if "new_bottom" in request.POST:

            bottom_form = BottomForm(data=request.POST)
            if bottom_form.is_valid() and request.is_ajax():
                bottom = Bottom.objects.create(bottom_form.cleaned_data)
                fit.bottom_set.add(bottom)
                request.session['bottom_count'] += 1

        if "new_shoe" in request.POST:

            shoe_form = ShoeForm(data=request.POST)
            if shoe_form.is_valid() and request.is_ajax():
                shoe = Shoe.objects.create(shoe_form.cleaned_data)
                fit.shoe_set.add(shoe)
                request.session['shoe_count'] += 1

        if "new_accessory" in request.POST:

            accessory_form = AccessoryForm(data=request.POST)
            if accessory_form.is_valid() and request.is_ajax():
                accessory = Accessory.objects.create(accessory_form.cleaned_data)
                fit.shoe_set.add(accessory)
                request.session['accessory_count'] += 1

    return render(request, 'fits/add_fit_elements.html', context)


@login_required
def like(request):
    fit_id = request.GET.get("likeId", "")
    user = request.user
    fit = Fit.objects.get(pk=fit_id)
    liked = False
    like = Like.objects.filter(user=user, fit=fit)
    if like:
        like.delete()
        like_count = fit.likes.count()

    else:
        liked = True
        Like.objects.create(user=user, fit=fit)
        like_count = fit.likes.count()
    resp = {
        'liked': liked,
        "like_amount": like_count,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


@login_required
def fun(request):
    id = request.GET.get("funId", "")
    try:
        fit = Fit.objects.get(shown_id__exact=id)
    except ObjectDoesNotExist:
        owner = User.objects.get(pk=id)
    else:
        owner = fit.owner

    is_following = False
    curr_user = request.user.profile
    followee = Profile.objects.get(user__username=owner)
    follower = followee.followers.all()
    if curr_user not in follower:
        is_following = True
        curr_user.following.add(followee)
        followee.followers.add(curr_user)
        print("Yayyy")

    else:
        curr_user.following.remove(followee)
        followee.followers.remove(curr_user)
        print("Yasssss")

    resp = {
        'is_following': is_following, }
    response = json.dumps(resp)

    return HttpResponse(response, content_type="application/json")


@login_required
def liked_fits(request, owner):
    liked_closet = Closet.objects.get(owner__username=owner, style__exact="liked_fits")
    if str(request.user) != owner:
        if liked_closet.private:
            raise Http404

    if request.method == 'POST':
        form = LikedFitsForm(request.POST, instance=liked_closet)
        if form.is_valid():
            form.save()

            return redirect('fits:liked_fits', owner=owner)
    else:
        form = LikedFitsForm(instance=liked_closet)
    liked_outfits = Fit.objects.filter(likes__user__username=owner).order_by('-date_added')

    owner = get_object_or_404(User, username=owner)
    context = {
        'liked_fits': liked_outfits,
        'owner': owner,
        'private_closet': liked_closet.private,
        'form': form
    }
    return render(request, 'fits/liked_fits.html', context)
