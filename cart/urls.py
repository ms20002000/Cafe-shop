from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('finalize/', views.finalize_cart, name='finalize_cart'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('order_history/', views.order_history, name='order_history'),
    path('checkout/', views.checkout, name='checkout'),
]
