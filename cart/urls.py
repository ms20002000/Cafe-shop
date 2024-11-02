from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart_test/', views.cart_detail, name='cart_detail'),
    path('add-multiple/', views.cart_add_multiple, name='cart_add_multiple'),
]
