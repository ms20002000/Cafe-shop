from order.models import Table
from django import forms
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
    


class OrderCreateForm(forms.Form):
    table = forms.ModelChoiceField(
        queryset=Table.available_tables(),
        label="انتخاب میز",
        empty_label="یک میز انتخاب کنید",
        required=True
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        label="شماره تلفن (اختیاری)",
        widget=forms.TextInput(attrs={'placeholder': 'مثلاً: 09123456789'})
    )
