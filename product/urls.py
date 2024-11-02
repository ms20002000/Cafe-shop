from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('update_category/<int:pk>/', CategoryUpdateView.as_view(), name='update_category'),
    path('<str:name>/', product_list, name='product_list'),  
    path('<str:name>/<str:product_name>/', product_detail, name='product_detail'),
]
