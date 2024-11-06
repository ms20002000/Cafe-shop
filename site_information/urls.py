from .views import *
from django.urls import path

urlpatterns = [
    path('', SiteInfoView.as_view(), name='site_info'),
]