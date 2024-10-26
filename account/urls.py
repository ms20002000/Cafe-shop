from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='home'),
    path('login/', StaffLogin.as_view(), name='staff_login'),
    path('manager_dashboard/', ManagerPanelView.as_view(), name='manager_dashboard'),
    path('staff_dashboard/', StaffDashboard.as_view(), name='staff_dashboard'),
    path('logout/', logout_user, name='logout'),
    path('change_password/', PasswordChange.as_view(), name='change_password'),
]