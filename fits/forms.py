from django import forms
from .models import Fit, Closet


class NewClosetForm(forms.ModelForm):
    class Meta:
        model = Closet
        fields = ['style', 'owner']


class NewFitForm(forms.ModelForm):
    class Meta:
        model = Fit
        fields = ['description', 'image', 'tags']


