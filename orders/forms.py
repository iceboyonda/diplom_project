from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note'].widget.attrs['maxlength'] = 150
        self.fields['note'].help_text = 'Максимум 150 символов.'

    def clean_phone(self):
        import re
        phone = self.cleaned_data['phone']
        # Разрешаем +7XXXXXXXXXX, 8XXXXXXXXXX, 7XXXXXXXXXX
        pattern = r'^(\+7|8|7)\d{10}$'
        if not re.match(pattern, phone):
            raise forms.ValidationError('Введите корректный номер телефона в формате +7XXXXXXXXXX или 8XXXXXXXXXX')
        return phone

    def clean_address(self):
        address = self.cleaned_data['address']
        # Минимум 5 символов, не только цифры
        if len(address.strip()) < 5 or address.strip().isdigit():
            raise forms.ValidationError('Введите корректный адрес доставки (не только цифры, минимум 5 символов)')
        return address

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        } 