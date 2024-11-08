from django.urls import path
from .views import *

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('tables/', TableListView.as_view(), name='table_list'),
    path('tables/create/', TableCreateView.as_view(), name='table_create'),
    path('tables/update/<int:pk>/', TableUpdateView.as_view(), name='table_update'),
]