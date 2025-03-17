from django import forms
from .models import *


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

class ExpensePlatformForm(forms.ModelForm):
    class Meta:
        model = ExpensePlatform
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items(): # empty_label
            field.widget.attrs['placeholder'] = field.label

            if isinstance(field, forms.ModelChoiceField):
                field.empty_label = field.label