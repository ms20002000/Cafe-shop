from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='customer_login'),
    path('register/', register, name='register'),
    # path('home/', home, name='home'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
    path('logout/', logout_user, name='logout'),
    path('permission-denied/', permission_denied_view, name='permission_denied'),
    path('list_user/', list_user, name='list_user'),
    path('edit_user/<int:id>/', edit_user, name='edit_user'),
    path('change_password/', PasswordChange.as_view(), name='change_password'),
]