from django import forms
from .models import Fit, Closet


class NewClosetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewClosetForm, self).__init__(*args, **kwargs)
        self.fields['style'].initial = ''

    class Meta:
        model = Closet
        fields = ['style']

    def clean(self):
        cleaned_data = super(NewClosetForm, self).clean()
        sty = self.cleaned_data.get('style')
        if sty in ['main_closet', 'new_closet']:
            raise forms.ValidationError(f'Cannot name closet {sty}')
        return cleaned_data


class NewFitForm(forms.ModelForm):
    class Meta:
        model = Fit
        fields = ['description', 'image', 'tags', 'closet']
