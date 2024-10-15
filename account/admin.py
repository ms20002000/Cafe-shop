from django.contrib import admin
from .models import RegularUser, StaffUser, ManagerUser

@admin.register(RegularUser)
class RegularUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'first_name', 'last_name', 'royalty_points')

@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'first_name', 'last_name', 'specialty')

@admin.register(ManagerUser)
class ManagerUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'first_name', 'last_name', 'specialty', 'department')
