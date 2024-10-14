from django.urls import path
from .views import *
from django.contrib.auth import views 

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]