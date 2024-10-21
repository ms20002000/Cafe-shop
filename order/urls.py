from django.urls import path

from .views import *

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
]