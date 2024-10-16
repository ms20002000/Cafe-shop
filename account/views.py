from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_admin:
                return redirect('admin_dashboard')  
            elif user.is_staff:
                return redirect('staff_dashboard')  
            else:
                return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})


def admin_required(user):
    return user.is_admin

@user_passes_test(admin_required)
def admin_dashboard(request):
    return render(request, 'account/admin_dashboard.html', {})

def staff_required(user):
    return user.is_staff

@user_passes_test(admin_required)
def staff_dashboard(request):
    return render(request, 'account/staff_dashboard.html', {})

def home(request):
    return render(request, 'account/home.html', {})


def admin_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                if user.is_admin:  
                    login(request, user)
                    return redirect('admin_dashboard')  
                else:
                    messages.error(request, 'You do not have admin privileges.')
            else:
                messages.error(request, 'Invalid phone number or password.') 
    else:
        form = CustomLoginForm()
    return render(request, 'account/admin_login.html', {'form': form})

def staff_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                if user.is_staff:  
                    login(request, user)
                    return redirect('staff_dashboard')  
                else:
                    messages.error(request, 'You do not have staff privileges.')
            else:
                messages.error(request, 'Invalid phone number or password.')

    else:
        form = CustomLoginForm()
    return render(request, 'account/staff_login.html', {'form': form})

def customer_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None and user.is_customer:
                login(request, user)
                return redirect('home')  
    else:
        form = CustomLoginForm()
    return render(request, 'account/login.html', {'form': form})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
    return render(request, 'account/logout.html', {})