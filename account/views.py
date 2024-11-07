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


class ManagerPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'account/manager_dashboard.html'

    def test_func(self):
        return self.request.user.is_admin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Top-selling items (filter by date if provided)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if not start_date:
            start_date = datetime.min  
        if not end_date:
            end_date = timezone.now() 

        products_queryset = Product.objects.filter(
            order_items__order__created_at__range=[start_date, end_date]
                    ).annotate(total_sold=Sum('order_items__quantity')
                                    ).order_by('-total_sold')
        context['top_items'] = products_queryset[:10]

        # Total Sales
        today = timezone.localtime(timezone.now()).date()
        one_day_ago = today - timedelta(days=1)
        one_month_ago = today - relativedelta(months=1)
        one_year_ago = today - relativedelta(years=1)

        # sales of today and yesterday
        daily_sales = Order.objects.filter(created_at__date=today).aggregate(
            daily_sales=Sum('total_price')
        )['daily_sales'] or 0

        yesterday_sales = Order.objects.filter(created_at__date=one_day_ago).aggregate(
            yesterday_sales=Sum('total_price')
        )['yesterday_sales'] or 0

        # sales of this month and last month
        monthly_sales = Order.objects.filter(
            created_at__date__gte=one_month_ago, created_at__date__lte=today
        ).aggregate(monthly_sales=Sum('total_price'))['monthly_sales'] or 0

        last_month_sales = Order.objects.filter(
            created_at__date__gte=(one_month_ago - relativedelta(months=1)), 
            created_at__date__lt=one_month_ago
        ).aggregate(last_month_sales=Sum('total_price'))['last_month_sales'] or 0

        # sales of this year and last year
        yearly_sales = Order.objects.filter(
            created_at__date__gte=one_year_ago, created_at__date__lte=today
        ).aggregate(yearly_sales=Sum('total_price'))['yearly_sales'] or 0

        last_year_sales = Order.objects.filter(
            created_at__date__gte=(one_year_ago - relativedelta(years=1)),
            created_at__date__lt=one_year_ago
        ).aggregate(last_year_sales=Sum('total_price'))['last_year_sales'] or 0

        # percentage change
        def calculate_percentage_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0  
            return round(((current - previous) / previous) * 100, 2) 

        # percentage change
        daily_sales_change = calculate_percentage_change(daily_sales, yesterday_sales)
        monthly_sales_change = calculate_percentage_change(monthly_sales, last_month_sales)
        yearly_sales_change = calculate_percentage_change(yearly_sales, last_year_sales)

        # 10-day sales list
        last_10_days = [(today - timedelta(days=i)).strftime("%b %d %Y") for i in range(9, -1, -1)]
        sales_last_10_days = [float(
            Order.objects.filter(created_at__date=today - timedelta(days=i)).aggregate(
                sales=Sum('total_price')
            )['sales'] or 0)
            for i in range(9, -1, -1)
        ]

        # 10-month sales list with "Jan 01 2022" format
        last_10_months = [
            (today - relativedelta(months=i)).replace(day=1).strftime("%b %d %Y") for i in range(9, -1, -1)
        ]
        sales_last_10_months = [float(
            Order.objects.filter(
                created_at__date__gte=(today - relativedelta(months=i)).replace(day=1),
                created_at__date__lt=(today - relativedelta(months=i-1)).replace(day=1)
            ).aggregate(sales=Sum('total_price'))['sales'] or 0)
            for i in range(9, -1, -1)
        ]

        sales_per_two_hour_intervals = []
        for hour in range(0, 24, 2):
            today = datetime.now()
            start_time = today.replace(hour=hour, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(hours=2)
            total_sales = Order.objects.filter(
                created_at__gte=start_time,
                created_at__lt=end_time
            ).aggregate(sales=Sum('total_price'))['sales'] or 0
            sales_per_two_hour_intervals.append(float(total_sales))
            
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
            'sales_per_two_hour_intervals':json.dumps(sales_per_two_hour_intervals)
        })


        # Sales by Category
        context['sales_by_category'] = Category.objects.annotate(
            total_sales=Sum('products__order_items__quantity')).order_by('-total_sales')

        # Sales by Time of Day (morning, afternoon, evening)
        today = timezone.localtime(timezone.now())
        morning_start = today.replace(hour=6, minute=0, second=0, microsecond=0)
        morning_end = today.replace(hour=12, minute=0, second=0, microsecond=0)
        afternoon_start = today.replace(hour=12, minute=0, second=0, microsecond=0)
        afternoon_end = today.replace(hour=18, minute=0, second=0, microsecond=0)
        evening_start = today.replace(hour=18, minute=0, second=0, microsecond=0)
        evening_end = today.replace(hour=23, minute=59, second=59, microsecond=0)

        context['morning_sales'] = Order.objects.filter(
            created_at__range=[morning_start, morning_end]).aggregate(
                total=Sum('total_price'))['total'] or 0
        context['afternoon_sales'] = Order.objects.filter(
            created_at__range=[afternoon_start, afternoon_end]).aggregate(
                total=Sum('total_price'))['total'] or 0
        context['evening_sales'] = Order.objects.filter(
            created_at__range=[evening_start, evening_end]).aggregate(
                total=Sum('total_price'))['total'] or 0

        # Customer Demographics
        context['total_customers'] = CustomUser.objects.filter(is_customer=True).count()

        # Sales by Customer
        sessions = Session.objects.all()
        sales_data = []
        for session in sessions:
            session_data = session.get_decoded()
            if session_data.get('order_id'):
                data = Order.objects.get(id=session_data.get('order_id'))
                sales_data.append(data)

        context['sales_by_customer'] = sales_data

        # Sales by Employee Report
        context['sales_by_employee'] = CustomUser.objects.filter(is_staff=True).annotate(
            total_orders_handled=Count('order'))

        # Peak Business Hour
        peak_hour_data = Order.objects.annotate(hour=ExtractHour('created_at')).values('hour').annotate(
            total_sales=Sum('total_price')).order_by('-total_sales').first()
        if peak_hour_data:
            context['peak_business_hour'] = peak_hour_data['hour']
            context['peak_business_hour_sales'] = peak_hour_data['total_sales']
        else:
            context['peak_business_hour'] = None
            context['peak_business_hour_sales'] = 0

        return context


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
        form = StaffAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  
            user.save()
            return redirect('staff_list')
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