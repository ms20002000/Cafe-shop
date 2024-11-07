from django.conf import settings
from django.test import TestCase, RequestFactory
from django.urls import reverse
from product.models import Product, Category
from order.models import Table
from .cart import Cart
from account.models import CustomUser

User = CustomUser  # Use the custom user model

class CartTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            phone_number='09123456789',
            password='password'
        )
        self.table = Table.objects.create(number=1, qr_code='QR12345')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            description='This is a test product.',
            category=self.category,
            product_photo='product_photos/default.jpg'
        )

    def test_cart_initialization(self):
        request = self.factory.get('/')
        request.COOKIES[settings.CART_COOKIE_NAME] = '{}'
        cart = Cart(request)
        self.assertEqual(len(cart), 0)

    def test_add_product_to_cart(self):
        request = self.factory.get('/')
        request.COOKIES[settings.CART_COOKIE_NAME] = '{}'
        cart = Cart(request)
        cart.add(self.product.id)  # اضافه کردن محصول به سبد خرید
        self.assertEqual(len(cart), 1)  # باید 1 باشد
        self.assertIn(str(self.product.id), cart.cart)

    def test_remove_product_from_cart(self):
        request = self.factory.get('/')
        request.COOKIES[settings.CART_COOKIE_NAME] = '{}'
        cart = Cart(request)
        cart.add(self.product.id)  # اضافه کردن محصول به سبد خرید
        self.assertEqual(len(cart), 1)

        cart.remove(self.product.id)  # حذف محصول از سبد خرید
        self.assertEqual(len(cart), 0)

    def test_update_product_quantity_in_cart(self):
        request = self.factory.get('/')
        request.COOKIES[settings.CART_COOKIE_NAME] = '{}'
        cart = Cart(request)
        cart.add(self.product.id)  # اضافه کردن محصول به سبد خرید
        self.assertEqual(len(cart), 1)

        cart.update_quantity(self.product.id, 2)  # فرض بر این است که متد update_quantity وجود دارد
        self.assertEqual(cart.cart[str(self.product.id)], 2)  # بررسی تعداد

    def test_cart_detail_view(self):
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 2})
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_checkout_view(self):
        self.user = User.objects.create_user(
            phone_number='1234567890',  
            password='testpass'
        )
        self.user.is_staff = True  # تنظیم کاربر به عنوان کاربر مدیر
        self.user.save()

        # ورود به سیستم با کاربر تستی
        login_success = self.client.login(phone_number='1234567890', password='testpass')
        # print(f"Login success: {login_success}")  # چاپ وضعیت ورود به سیستم

        response = self.client.get(reverse('order_create'))
        # print(response.content)  # چاپ محتوای پاسخ
        self.assertEqual(response.status_code, 200)



    def test_finalize_cart(self):
        request = self.factory.get('/')
        request.COOKIES[settings.CART_COOKIE_NAME] = '{}'
        cart = Cart(request)
        self.assertEqual(len(cart), 0)

    def test_order_history_view(self):
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 2})
        self.client.post(reverse('finalize_cart'), {
            'table': self.table.id,
            'phone_number': '09123456789',
            'payment_method': 'cash'
        })
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_order_summary_view(self):
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 2})
        response = self.client.post(reverse('finalize_cart'), {
            'table': self.table.id,
            'phone_number': '09123456789',
            'payment_method': 'cash'
        })
        order_id = response.wsgi_request.session.get('order_id')
        response = self.client.get(reverse('order_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')  # Check if the product appears in order summary

    def test_update_product_quantity_in_cart(self):
        request = self.factory.get('/')
        cart = Cart(request)
        cart.add(self.product.id, quantity=1)
        cart.update_quantity(self.product.id, 2)  # به‌روزرسانی مقدار به 2
        self.assertEqual(cart.cart[str(self.product.id)]['quantity'], 2)  # بررسی مقدار جدید
