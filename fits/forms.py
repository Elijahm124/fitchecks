from django import forms
from .models import Fit, Closet


class ClosetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClosetForm, self).__init__(*args, **kwargs)
        self.fields['style'].initial = ''

    class Meta:
        model = Closet
        fields = ['style']

    def clean(self):
        cleaned_data = super(ClosetForm, self).clean()
        sty = self.cleaned_data.get('style')
        if sty in ['main_closet', 'new_closet']:
            raise forms.ValidationError(f'Cannot name closet {sty}')
        return cleaned_data


class FitForm(forms.ModelForm):
    class Meta:
        model = Fit
        fields = ['description', 'image', 'tags', 'closet']

    closet = forms.ModelMultipleChoiceField(
        queryset=Closet.objects.exclude(style__exact='main_closet'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
