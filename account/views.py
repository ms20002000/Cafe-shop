from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, AdminUserEditForm, UserEditForm
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.views import View
from django.views.generic import ListView
from order.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.dateparse import parse_date


class StaffLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=phone_number, password=password)
            
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('staff_dashboard')
            else:
                messages.error(request, 'Invalid credentials or not a staff member')
                return redirect('staff_login')


class StaffDashboard(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'account/staff_dashboard.html'
    model = Order
    context_object_name = 'orders'

    def test_func(self):
        return self.request.user.is_staff 

    def get_queryset(self):
        queryset = Order.objects.all()
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        search_query = self.request.GET.get('phone_number')
        if search_query:
            queryset = queryset.filter(customer__phone_number__icontains=search_query)

        table_number = self.request.GET.get('table_number')
        if table_number:
            queryset = queryset.filter(table__number=table_number)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_name'] = self.request.user.first_name
        return context


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