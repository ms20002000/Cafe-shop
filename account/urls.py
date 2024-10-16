from django.urls import path
from .views import *

urlpatterns = [
    path('login/', customer_login, name='customer_login'),
    path('register/', register, name='register'),
    path('staff_login/', staff_login, name='staff_login'),
    path('admin_login/', admin_login, name='admin_login'),
    path('home/', home, name='home'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
    path('logout/', logout_user, name='logout'),
]