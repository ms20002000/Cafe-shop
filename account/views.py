from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, AdminUserEditForm, UserEditForm
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('admin_dashboard')
            elif user is not None and user.is_staff:
                login(request, user)
                return redirect('staff_dashboard')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('home')  
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
    return render(request, 'account/logout.html', {})


def permission_denied_view(request):
    return render(request, 'account/permission_denied.html', {})

def admin_required(user):
    return user.is_authenticated and user.is_admin 

@user_passes_test(admin_required, login_url='permission_denied')
def admin_dashboard(request):
    return render(request, 'account/admin_dashboard.html', {})

def staff_required(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(staff_required, login_url='permission_denied')
def staff_dashboard(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('staff_dashboard')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'account/staff_dashboard.html', {'form': form})

# def home(request):
#     return render(request, 'account/home.html', {})

@user_passes_test(admin_required, login_url='permission_denied')
def list_user(request):
    users = CustomUser.objects.all()
    return render(request, 'account/list_users.html', {'users': users})

@user_passes_test(admin_required, login_url='permission_denied')
def edit_user(request, id):
    user = get_object_or_404(CustomUser, id=id)  
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()  
            messages.success(request, 'User details updated successfully!')
            return redirect('list_user')  
    else:
        form = AdminUserEditForm(instance=user)  
    return render(request, 'account/edit_user.html', {'form': form})

class PasswordChange(PasswordChangeView):
    template_name = 'account/change_password.html'
    def form_valid(self, form):
        user = self.request.user
        form.save()  

        if user.is_admin:
            return redirect('admin_dashboard')  
        elif user.is_staff:
            return redirect('staff_dashboard')  
        else:
            return redirect('home')