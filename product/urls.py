from django.urls import path
from .views import *


urlpatterns = [
    path('', category_list, name='category_list'),
    path('<int:id>/', category_detail, name='category_detail'),
    path('<int:id>/<int:product_id>/', product_detail, name='product_detail'),
]