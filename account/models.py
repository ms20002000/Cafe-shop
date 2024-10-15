from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    groups = models.ManyToManyField(
        Group,
        related_name="baseuser_set",  
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="baseuser_permissions", 
        blank=True,
    )

class RegularUser(User):
    royalty_points = models.IntegerField(default=0)

class StaffUser(User):
    specialty = models.CharField(max_length=100)

class ManagerUser(StaffUser):
    department = models.CharField(max_length=100)