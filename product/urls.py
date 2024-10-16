from django.urls import path
from .views import *


urlpatterns = [
    path('', category_list, name='category_list'),
    path('<int:id>/', product_list, name='product_list'),
    path('<int:id>/<int:product_id>/', product_detail, name='product_detail'),
]