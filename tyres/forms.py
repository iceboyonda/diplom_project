from django import forms
from .models import TyreModel, TyreVariant, RimModel, RimVariant
from django.forms import inlineformset_factory

class TyreVariantForm(forms.ModelForm):
    class Meta:
        model = TyreVariant
        fields = ['width', 'profile', 'radius', 'season', 'studded', 'speed_index', 'price', 'stock']

    def clean(self):
        cleaned_data = super().clean()
        season = cleaned_data.get('season')
        studded = cleaned_data.get('studded')
        model = self.instance.model # Получаем модель шины, к которой относится вариант

        if model and season is not None and studded is not None:
            # Находим все другие варианты этой же модели с тем же сезоном
            conflicting_variants = model.variants.filter(
                season=season
            ).exclude(pk=self.instance.pk) # Исключаем текущий вариант, если он уже существует

            # Проверяем, есть ли среди них варианты с противоположным значением studded
            if conflicting_variants.filter(studded=not studded).exists():
                raise forms.ValidationError(
                    f"Все варианты модели {model.name} в сезоне '{self.instance.get_season_display()}' должны быть либо шипованными, либо нешипованными."
                )

        return cleaned_data

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
    form=TyreVariantForm,
    extra=1, can_delete=True
)

class RimModelForm(forms.ModelForm):
    class Meta:
        model = RimModel
        fields = ['brand', 'name', 'description', 'image']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Бренд'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

RimVariantFormSet = inlineformset_factory(
    RimModel, RimVariant,
    fields=['diameter', 'width', 'bolt_pattern', 'offset', 'dia', 'color', 'material', 'price', 'stock', 'image'],
    extra=1,
    can_delete=True,
    widgets={
        'diameter': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
        'width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
        'bolt_pattern': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: 5x114.3'}),
        'offset': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: ET45'}),
        'dia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: 60.1'}),
        'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Серебристый'}),
        'material': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Алюминий'}),
        'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
    }
) 