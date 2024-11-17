import json
import xlsxwriter
from order.models import Order, OrderItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, StaffAddForm, StaffUpdateForm
from django.views.generic.edit import UpdateView
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.views import View
from django.views.generic import ListView, TemplateView
from order.models import Order, Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.dateparse import parse_date
from django.db.models import Count, Sum, F
from django.utils import timezone
from django.urls import reverse_lazy
import csv
from django.http import HttpResponse
from django.db.models.functions import ExtractHour
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.sessions.models import Session

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
            if user is not None:
                login(request, user)
                if user.is_admin:
                    return redirect('manager_dashboard')
                elif user.is_staff:
                    return redirect('staff_dashboard')
            else:
                messages.error(request, 'Invalid credentials or not a staff member')
        else:
            messages.error(request, 'شماره همراه یا رمز عبور صحیح نمی‌باشد')
            
        return render(request, 'account/login.html', {'form': form})


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

        queryset = queryset.order_by('created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_name'] = self.request.user.first_name
        return context


def logout_user(request):
    logout(request)
    return redirect('home')



class ManagerPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'account/manager_dashboard.html'

    def test_func(self):
        return self.request.user.is_admin

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Date filtering for top-selling items
        start_date = self.request.GET.get('start_date', datetime(1970, 1, 1))
        end_date = self.request.GET.get('end_date', timezone.now())

        top_products = Product.objects.filter(
            order_items__order__created_at__range=[start_date, end_date]
        ).annotate(total_sold=Sum('order_items__quantity')).order_by('-total_sold')
        context['top_items'] = top_products[:10]

        # Date calculations
        today = timezone.localtime(timezone.now()).date()
        one_day_ago = today - timedelta(days=1)
        one_month_ago = today - relativedelta(months=1)
        one_year_ago = today - relativedelta(years=1)

        # Daily, monthly, yearly sales calculations
        daily_sales = self.get_sales_sum(today)
        yesterday_sales = self.get_sales_sum(one_day_ago)
        monthly_sales = self.get_sales_sum(one_month_ago, today)
        last_month_sales = self.get_sales_sum(one_month_ago - relativedelta(months=1), one_month_ago)
        yearly_sales = self.get_sales_sum(one_year_ago, today)
        last_year_sales = self.get_sales_sum(one_year_ago - relativedelta(years=1), one_year_ago)

        # Percentage changes
        daily_sales_change = self.calculate_percentage_change(daily_sales, yesterday_sales)
        monthly_sales_change = self.calculate_percentage_change(monthly_sales, last_month_sales)
        yearly_sales_change = self.calculate_percentage_change(yearly_sales, last_year_sales)

        # 10-day and 10-month sales lists
        last_10_days, sales_last_10_days = self.get_sales_last_10_days(today)
        last_10_months, sales_last_10_months = self.get_sales_last_10_months(today)

        # Two-hour interval sales
        sales_per_two_hour_intervals = self.get_sales_per_two_hour_intervals()

        # Sales by category
        context['sales_by_category'] = Category.objects.annotate(
            total_sales=Sum('products__order_items__quantity')
        ).order_by('-total_sales')

        # Sales by time of day
        context.update(self.get_sales_by_time_of_day(today))

        # Customer and employee sales data
        context['total_customers'] = CustomUser.objects.filter(is_customer=True).count()
        context['sales_by_customer'] = self.get_sales_by_customer()
        context['sales_by_employee'] = CustomUser.objects.filter(is_staff=True).annotate(
            total_orders_handled=Count('order')
        )

        # Peak business hour
        peak_hour_data = self.get_peak_business_hour()
        context.update(peak_hour_data)

        # Updating context with sales data and metrics
        context.update({
            'daily_sales': daily_sales,
            'monthly_sales': monthly_sales,
            'yearly_sales': yearly_sales,
            'daily_sales_change': daily_sales_change,
            'monthly_sales_change': monthly_sales_change,
            'yearly_sales_change': yearly_sales_change,
            'last_10_days': json.dumps(last_10_days),
            'sales_last_10_days': json.dumps(sales_last_10_days),
            'last_10_months': json.dumps(last_10_months),
            'sales_last_10_months': json.dumps(sales_last_10_months),
            'sales_per_two_hour_intervals': json.dumps(sales_per_two_hour_intervals),
        })

        return context

    def get_sales_sum(self, start_date, end_date=None):
        if not end_date:
            end_date = start_date
        return Order.objects.filter(
            created_at__date__range=[start_date, end_date], 
            status=Order.StatusOrder.COMPLETED
        ).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0

    def calculate_percentage_change(self, current, previous):
        if previous == 0:
            return 100 if current > 0 else 0
        return round(((current - previous) / previous) * 100, 2)

    def get_sales_last_10_days(self, today):
        last_10_days = [(today - timedelta(days=i)).strftime("%b %d %Y") for i in range(9, -1, -1)]
        sales_last_10_days = [
            float(self.get_sales_sum(today - timedelta(days=i))) for i in range(9, -1, -1)
        ]
        return last_10_days, sales_last_10_days

    def get_sales_last_10_months(self, today):
        last_10_months = [
            (today - relativedelta(months=i)).replace(day=1).strftime("%b %d %Y") for i in range(9, -1, -1)
        ]
        sales_last_10_months = [
            float(self.get_sales_sum(
                (today - relativedelta(months=i)).replace(day=1),
                (today - relativedelta(months=i - 1)).replace(day=1)
            )) for i in range(9, -1, -1)
        ]
        return last_10_months, sales_last_10_months

    def get_sales_per_two_hour_intervals(self):
        sales_per_two_hour_intervals = []
        start_of_day = timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)        
        for hour in range(0, 24, 2):
            start_time = start_of_day + timedelta(hours=hour)
            end_time = start_time + timedelta(hours=2)            
            total_sales = Order.objects.filter(
                created_at__gte=start_time,
                created_at__lt=end_time,
                status=Order.StatusOrder.COMPLETED
            ).aggregate(sales=Sum('total_price'))['sales'] or 0
            
            sales_per_two_hour_intervals.append(float(total_sales))
        
        return sales_per_two_hour_intervals

    def get_sales_by_time_of_day(self, today):
        time_periods = {
            'morning_sales': (6, 12),
            'afternoon_sales': (12, 18),
            'evening_sales': (18, 23)
        }
        sales_by_time = {}
        for period, (start_hour, end_hour) in time_periods.items():
            start_time = timezone.localtime(timezone.now()).replace(hour=start_hour, minute=0, second=0, microsecond=0)
            if end_hour == 23:
                end_time = timezone.localtime(timezone.now()).replace(hour=end_hour, minute=59, second=59, microsecond=999999)
            else:
                end_time = timezone.localtime(timezone.now()).replace(hour=end_hour, minute=0, second=0, microsecond=0)
            sales_by_time[period] = Order.objects.filter(
                created_at__range=[start_time, end_time], 
                status=Order.StatusOrder.COMPLETED
            ).aggregate(total=Sum('total_price'))['total'] or 0
        return sales_by_time

    def get_sales_by_customer(self):
        sales_data = []
        sessions = Session.objects.all()
        for session in sessions:
            session_data = session.get_decoded()
            if session_data.get('order_id'):
                order = Order.objects.filter(id=session_data.get('order_id')).first()
                if order:
                    sales_data.append(order)
        return sales_data

    def get_peak_business_hour(self):
        peak_data = Order.objects.annotate(hour=ExtractHour('created_at')).values('hour').annotate(
            total_sales=Sum('total_price')
        ).order_by('-total_sales').first()
        return {
            'peak_business_hour': peak_data['hour'] if peak_data else None,
            'peak_business_hour_sales': peak_data['total_sales'] if peak_data else 0
        }

    


class ExportSalesReportView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_admin

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'

        workbook = xlsxwriter.Workbook(response, {'in_memory': True})

        orders = Order.objects.all().order_by('created_at')  
        order_items = OrderItem.objects.all().order_by('order__created_at')  

        # sheet 1
        orders_sheet = workbook.add_worksheet('Orders')
        orders_headers = ['Order ID', 'Customer', 'Employee', 'Total Price', 'Status', 'Created At']
        for col_num, header in enumerate(orders_headers):
            orders_sheet.write(0, col_num, header)

        for row_num, order in enumerate(orders, start=1):
            orders_sheet.write(row_num, 0, order.id)
            orders_sheet.write(row_num, 1, order.modify_by.phone_number if order.modify_by else '')
            orders_sheet.write(row_num, 2, order.modify_by.first_name if order.modify_by else '')
            orders_sheet.write(row_num, 3, order.total_price)
            orders_sheet.write(row_num, 4, order.status)
            orders_sheet.write(row_num, 5, order.created_at.strftime('%Y-%m-%d %H:%M'))

        # sheet 2
        order_items_sheet = workbook.add_worksheet('Order Items')
        order_items_headers = ['Order ID', 'Product', 'Quantity', 'Unit Price', 'Total Price', 'Order Created At']
        for col_num, header in enumerate(order_items_headers):
            order_items_sheet.write(0, col_num, header)

        for row_num, item in enumerate(order_items, start=1):
            order_items_sheet.write(row_num, 0, item.order.id)
            order_items_sheet.write(row_num, 1, item.product.name if item.product else '')
            order_items_sheet.write(row_num, 2, item.quantity)
            order_items_sheet.write(row_num, 3, item.product.price)
            order_items_sheet.write(row_num, 4, item.quantity * item.product.price)
            order_items_sheet.write(row_num, 5, item.order.created_at.strftime('%Y-%m-%d %H:%M'))

        # sheet 3
        summary_sheet = workbook.add_worksheet('Sales Summary')

        today = timezone.localtime(timezone.now()).date()
        one_month_ago = today - timedelta(days=30)  
        one_year_ago = today - timedelta(days=365)  

        summary_data = {
            'Total Sales': Order.objects.aggregate(total_sales=Sum('total_price'))['total_sales'] or 0,
            
            'Daily Sales': Order.objects.filter(
                created_at__date=today
            ).aggregate(daily_sales=Sum('total_price'))['daily_sales'] or 0,

            'Monthly Sales': Order.objects.filter(
                created_at__date__gte=one_month_ago, created_at__date__lte=today
            ).aggregate(monthly_sales=Sum('total_price'))['monthly_sales'] or 0,

            'Yearly Sales': Order.objects.filter(
                created_at__date__gte=one_year_ago, created_at__date__lte=today
            ).aggregate(yearly_sales=Sum('total_price'))['yearly_sales'] or 0,
        }

        summary_headers = ['Metric', 'Amount']
        for col_num, header in enumerate(summary_headers):
            summary_sheet.write(0, col_num, header)

        for row_num, (metric, amount) in enumerate(summary_data.items(), start=1):
            summary_sheet.write(row_num, 0, metric)
            summary_sheet.write(row_num, 1, amount)

        workbook.close()
        return response


class AddStaffView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'account/add_staff.html'

    def test_func(self):
        return self.request.user.is_admin  

    def get(self, request):
        form = StaffAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StaffAddForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  
            user.save()
            messages.success(request, 'کاربر با موفقیت اضافه شد.')
            return redirect('staff_list')
        messages.error(request, 'لطفاً خطاهای زیر را بررسی کنید.')
        return render(request, self.template_name, {'form': form})


class StaffListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'account/staff_list.html'
    context_object_name = 'staff_list'

    def get_queryset(self):
        return CustomUser.objects.filter(is_staff=True)

    def test_func(self):
        return self.request.user.is_admin


class StaffUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = StaffUpdateForm
    template_name = 'account/update_staff.html'
    success_url = reverse_lazy('staff_list')

    def test_func(self):
        return self.request.user.is_admin