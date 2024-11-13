from django import forms
from .models import Order, OrderItem, Table, Product
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

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].empty_label = "------"
        if not self.instance.pk:  
            self.fields['product'].initial = None

OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,  
                                          extra=1, can_delete=True)

UpdateOrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                          extra=0, can_delete=True)

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'qr_code']