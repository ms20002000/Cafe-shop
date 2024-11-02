from django.shortcuts import redirect
from django.urls import reverse

class RestrictStaffAdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')) and request.user.is_authenticated:
            if request.user.is_staff and not request.user.is_admin:
                return redirect('home')  

        response = self.get_response(request)
        return response
