
# tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Order, Table, OrderItem
from .forms import OrderForm, OrderItemFormSet, TableForm
from product.models import Product

User = get_user_model()

class OrderCreateViewTests(TestCase):
    def setUp(self):
        # ایجاد کاربر و لاگین کردن
        self.user = User.objects.create_user(
            phone_number='09123456789', 
            password='testpass', 
            is_staff=True
        )
        self.client.login(phone_number='09123456789', password='testpass')

        # ایجاد یک جدول برای استفاده در سفارش
        self.table = Table.objects.create(number=1, qr_code="sample_qr_code")

    def test_order_create_view_get(self):
        url = reverse('order_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/create_order.html')
        self.assertIn('form', response.context)
        self.assertIn('formset', response.context)

    def test_order_create_view_post(self):
        response = self.client.post(reverse('order_create'), {
            'status': 'P',  # وضعیت سفارش
            'payment_method': 'C',  # روش پرداخت
            'table': self.table.id,  # ارجاع به جدول ایجاد شده در setUp
        })
        self.assertEqual(response.status_code, 302)  # بررسی انتقال به صفحه دیگر بعد از موفقیت

class TableCreateViewTests(TestCase):
    def setUp(self):
        # ایجاد کاربر و لاگین کردن با phone_number به جای username
        self.user = User.objects.create_user(
            phone_number='09123456789', 
            password='testpass', 
            is_admin=True
        )
        self.client.login(phone_number='09123456789', password='testpass')

    def test_table_create_view_get(self):
        url = reverse('table_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/table_form.html')
        self.assertIn('form', response.context)

    def test_table_create_view_post(self):
        url = reverse('table_create')
        data = {
            'number': 1,
            'qr_code': '123456',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Table.objects.count(), 1)
