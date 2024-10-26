from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, AdminUserEditForm, UserEditForm
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.views import View
from django.views.generic import ListView, TemplateView
from order.models import Order, Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.dateparse import parse_date
from django.db.models import Count, Sum, F
from datetime import datetime, timedelta


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
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('manager_dashboard')
            elif user is not None and user.is_staff:
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
            queryset = queryset.filter(modify_by__phone_number__icontains=search_query)

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

def HomeView(request):
    return render(request, 'account/home.html', {})





class ManagerPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'account/manager_dashboard.html'

    def test_func(self):
        return self.request.user.is_admin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Top-selling items (filter by date if provided)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        products_queryset = Product.objects.annotate(total_sold=Sum('order_items__quantity')).order_by('-total_sold')
        if start_date and end_date:
            products_queryset = products_queryset.filter(order_items__order__created_at__range=[start_date, end_date])
        context['top_items'] = products_queryset[:10]  # top 10 items

        # Total Sales
        context['total_sales'] = Order.objects.aggregate(total_sales=Sum('total_price'))['total_sales'] or 0

        # Daily, Monthly, and Yearly Sales
        today = datetime.today()
        context['daily_sales'] = Order.objects.filter(created_at__date=today).aggregate(daily_sales=Sum('total_price'))['daily_sales'] or 0
        context['monthly_sales'] = Order.objects.filter(created_at__month=today.month, created_at__year=today.year).aggregate(monthly_sales=Sum('total_price'))['monthly_sales'] or 0
        context['yearly_sales'] = Order.objects.filter(created_at__year=today.year).aggregate(yearly_sales=Sum('total_price'))['yearly_sales'] or 0

        # Sales by Category
        context['sales_by_category'] = Category.objects.annotate(total_sales=Sum('products__order_items__quantity')).order_by('-total_sales')

        # Sales by Time of Day (e.g., morning, afternoon, evening)
        morning_start, morning_end = today.replace(hour=6, minute=0), today.replace(hour=12, minute=0)
        afternoon_start, afternoon_end = today.replace(hour=12, minute=0), today.replace(hour=18, minute=0)
        evening_start, evening_end = today.replace(hour=18, minute=0), today.replace(hour=23, minute=59)
        context['morning_sales'] = Order.objects.filter(created_at__range=[morning_start, morning_end]).aggregate(total=Sum('total_price'))['total'] or 0
        context['afternoon_sales'] = Order.objects.filter(created_at__range=[afternoon_start, afternoon_end]).aggregate(total=Sum('total_price'))['total'] or 0
        context['evening_sales'] = Order.objects.filter(created_at__range=[evening_start, evening_end]).aggregate(total=Sum('total_price'))['total'] or 0

        # Customer Demographics
        context['total_customers'] = CustomUser.objects.filter(is_customer=True).count()

        return context
