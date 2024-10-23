from django import forms
from .models import Order, OrderItem
from django.forms.models import inlineformset_factory

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'payment_method', 'table'] 

OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('product', 'quantity'),
                                          extra=3, can_delete=True)
