from django import forms
from .models import TyreModel, TyreVariant
from django.forms import inlineformset_factory

class TyreModelForm(forms.ModelForm):
    class Meta:
        model = TyreModel
        fields = ['brand', 'name', 'description', 'image']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Бренд'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

TyreVariantFormSet = inlineformset_factory(
    TyreModel, TyreVariant,
    fields=['width', 'profile', 'radius', 'season', 'studded', 'speed_index', 'price', 'stock'],
    extra=1, can_delete=True
) 