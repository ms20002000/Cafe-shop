from django import forms
from .models import Order, OrderItem, Table
from django.forms.models import inlineformset_factory

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'payment_method', 'table'] 

    def __init__(self, *args, **kwargs):
        is_update = kwargs.pop('is_update', False)
        super().__init__(*args, **kwargs)
        if not is_update:
            self.fields['table'].queryset = Table.available_tables()

OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('product', 'quantity'),
                                          extra=1, can_delete=True)

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'qr_code']