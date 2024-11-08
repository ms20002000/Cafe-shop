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
        if is_update:
            available_tables = Table.available_tables()
            reserved_table_by_user = Table.objects.filter(id=self.instance.table.id) if self.instance.table else Table.objects.none()
            self.fields['table'].queryset = (available_tables | reserved_table_by_user).distinct()
        else:
            self.fields['table'].queryset = Table.available_tables()

OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('product', 'quantity'),
                                          extra=3, can_delete=True)

UpdateOrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('product', 'quantity'),
                                          extra=1, can_delete=True)

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'qr_code']