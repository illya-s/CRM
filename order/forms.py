from django import forms
from .models import *


def get_model_choices():
    models_to_include = ['product.MyProduct', 'product.Product']
    content_types = ContentType.objects.filter(
        app_label__in=[model.split('.')[0] for model in models_to_include],
        model__in=[model.split('.')[1].lower() for model in models_to_include]
    )
    return content_types

class OrderForm(forms.ModelForm):
    remove_client_check = forms.BooleanField(required=False, label='Удалить изображение')
    remove_bank_check   = forms.BooleanField(required=False, label='Удалить изображение')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label
        self.fields['product'].label_from_instance = lambda obj: f"{obj.name} - {obj.article}"

    class Meta:
        model = Order
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('remove_client_check') and instance.client_check:
            instance.client_check.delete(save=False)
            instance.client_check = None
        if self.cleaned_data.get('remove_bank_check') and instance.bank_check:
            instance.bank_check.delete(save=False)
            instance.bank_check = None

        if commit:
            instance.save()
        return instance

class SenderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"