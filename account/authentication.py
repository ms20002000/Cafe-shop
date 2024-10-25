from .models import CustomUser
from django.contrib.auth.backends import BaseBackend

class PhoneNumberAuthBackend(BaseBackend):
    """
    Authenticate using phone number and password.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(phone_number=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
