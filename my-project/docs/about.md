________________________________________
Project Name: Cafe Shop

Overview

The Cafe Shop project is a web application built with Django that allows users to browse and purchase products in an online cafe. The application has features such as user authentication, product management, order processing, and a shopping cart.

Technologies Used

•	Django

•	Python 3.x

•	PostgreSQL

•	HTML/CSS
________________________________________
Installation Instructions

1.	Clone the repository:

git clone https://github.com/ms20002000/Cafe-shop.git

2.	Navigate to the project directory:

cd cafe-shop

3.	Create a virtual environment:

python3 -m venv venv

4.	Install the required dependencies:

pip install -r requirements.txt

5.	Set up the PostgreSQL database:

o	Ensure PostgreSQL is installed and running.

o	Create a new database for the project.

6.	Update settings.py with your database credentials.

7.	Run migrations:
python manage.py migrate
________________________________________

Key Features

•	User Authentication: Users can sign up, log in, 
and log out.

•	Product Management: Admins can add, update, and delete products.

•	Shopping Cart: Users can add products to their cart and place orders.

•	Order Tracking: Users can track their order status.
________________________________________
Folder Structure

CAFE-SHOP/
│
├── account/
│   ├── __init__.py/
│   ├── admin.py/
│   ├── apps.py/
│   ├── authentication.py/
│   ├── forms.py/
│   ├── middleware.py/
│   ├── models.py/
│   ├── tests.py/
│   ├── urls.py/
│   └── views.py/
│
├── cafe_shop/
│   ├── __init__.py/
│   ├── asgi.py/
│   ├── settings.py/
│   ├── urls.py/
│   └── wsgi.py/
│
├── cart/
│   ├── __init__.py/
│   ├── admin.py/
│   ├── apps.py/
│   ├── cart.py/
│   ├── forms.py/
│   ├── models.py/
│   ├── tests.py/
│   ├── urls.py/
│   └── views.py/
│
├── document/
│
├── erd/
│
├── media/
│
├── order/
│   ├── __init__.py/
│   ├── admin.py/
│   ├── apps.py/
│   ├── forms.py/
│   ├── models.py/
│   ├── signals.py/
│   ├── tests.py/
│   ├── urls.py/
│   └── views.py/
│
│
├── product/
│   ├── __init__.py/
│   ├── admin.py/
│   ├── apps.py/
│   ├── forms.py/
│   ├── models.py/
│   ├── tests.py/
│   ├── urls.py/
│   └── views.py/
│
│
├── site_information/
│   ├── __init__.py/
│   ├── admin.py/
│   ├── apps.py/
│   ├── context_processors.py.py/
│   ├── forms.py/
│   ├── models.py/
│   ├── tests.py/
│   ├── urls.py/
│   └── views.py/
│
│
├── static/
│   ├── main/
│   └── staff/
│
├── templates/
│   ├── base.html
│   └── staff-base.html
│
├── manage.py
│
├── README.md
│
└── requirements.txt
________________________________________
API Endpoints

1.	POST /api/login - Login endpoint.

2.	POST /api/signup - Signup endpoint.

3.	GET /api/products - Fetch a list of products.

4.	POST /api/order - Place an order.
________________________________________
Future Enhancements

•	Payment Integration: Add support for credit card payments.
________________________________________
Contributors

•	Amir - Project Manager

•	Mohammad - Backend Developer

•	Parsa - Backend Developer

•	Faraz - Frontend Developer
