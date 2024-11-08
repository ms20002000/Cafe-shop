from django.urls import path
from .views import *

urlpatterns = [
    path('login/', StaffLogin.as_view(), name='staff_login'),
    path('manager_dashboard/', ManagerPanelView.as_view(), name='manager_dashboard'),
    path('staff_list/', StaffListView.as_view(), name='staff_list'),
    path('update_staff/<int:pk>', StaffUpdateView.as_view(), name='update_staff'),
    path('add_staff/', AddStaffView.as_view(), name='add_staff'),
    path('staff_dashboard/', StaffDashboard.as_view(), name='staff_dashboard'),
    path('logout/', logout_user, name='logout'),
    path('export_sales_report/', ExportSalesReportView.as_view(), name='export_sales_report'),
]