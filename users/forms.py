from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'weight', 'height','gender']
        labels = {"weight": "Weight, Enter in lbs.",
                  "height": "Height, Enter in inches"}
