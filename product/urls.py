from django.urls import path
from .views import *


urlpatterns = [
    path('', category_list, name='home'),
    path('<int:id>/', product_list, name='product_list'),
    path('<int:id>/<int:product_id>/', product_detail, name='product_detail'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('update_category/<int:pk>/', CategoryUpdateView.as_view(), name='update_category'),
]