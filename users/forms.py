from django import forms
from .models import Profile
from django_countries.widgets import CountrySelectWidget


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'weight', 'height', 'gender', 'country']
        labels = {"weight": "Weight, Enter in lbs.",
                  "height": "Height, Enter in inches"}
        widgets = {'country': CountrySelectWidget()}
