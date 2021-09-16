from django import forms
from django.forms import modelformset_factory
from .models import Fit, Closet, Top, Bottom, Accessory, Shoe, Comment


class ClosetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClosetForm, self).__init__(*args, **kwargs)
        self.fields['style'].initial = ''

    class Meta:
        model = Closet
        fields = ['style', 'private']

    def clean(self):
        cleaned_data = super(ClosetForm, self).clean()
        sty = self.cleaned_data.get('style')
        if sty in ['main_closet', 'new_closet']:
            raise forms.ValidationError(f'Cannot name closet {sty}')
        return cleaned_data


class FitForm(forms.ModelForm):
    class Meta:
        model = Fit
        fields = ['description', 'image', 'tags', 'closet', 'private']

    closet = forms.ModelMultipleChoiceField(
        queryset=Closet.objects.exclude(style__exact='main_closet'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class TopForm(forms.ModelForm):
    class Meta:
        model = Top
        fields = ['brand', 'size', 'color', 'description', 'price']


class BottomForm(forms.ModelForm):
    class Meta:
        model = Bottom
        fields = ['brand', 'size', 'color', 'description', 'price']


class ShoeForm(forms.ModelForm):
    class Meta:
        model = Shoe
        fields = ['brand', 'size', 'color', 'description', 'price']


class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['brand', 'size', 'color', 'description', 'price']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


AccessoryFormSet = modelformset_factory(
    Accessory, fields=('brand', 'size', 'color', 'description', 'price'), extra=0
)
