from django.urls import path

from .views import *
from . import views

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
]


app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
]

urlpatterns = [
    path('order-history/', views.order_history, name='order_history'),
]
