from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'first_name', 'last_name',
                     'is_staff', 'is_active', 'is_customer', 'is_admin', 'is_superuser')