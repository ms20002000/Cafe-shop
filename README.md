
# 🌟 Cafe Shop: Django Project 🌟

Welcome to the **Cafe Shop**, a Django full-stack web application designed to manage a cafe's online presence. This project aims to build a fully functional web application for a cafe that includes an online menu for customers, an administrative staff panel, sales analytics, and much more. 

## Features

### Customer-Facing Features:
- **Browse Menu**: Customers can explore cafe menu items by category.
- **Order Placement**: Users can add items to the cart and place orders.
- **Mobile-Friendly**: Responsive design optimized for mobile devices.

### Staff and Manager Features:
- **Order Management**: Staff can view and manage customer orders.
- **Menu Management**: Admin users can update menu items and categories.
- **Sales Analytics**: Managers have access to key sales metrics, reports, and customer data.

## Tech Stack
- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript and BS base (with animations and transitions)
- **Version Control**: Git (GitHub repository)

## Setup Instructions

### Prerequisites:
- Python 3.x
- PostgreSQL
- Git

### Installation Steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/ms20002000/cafe-shop.git
    cd cafe-shop
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database:
    - Create a PostgreSQL database and update the `DATABASES` setting in the `settings.py` file with your credentials.
    - Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Access the site at `http://127.0.0.1:8000/`.

## Project Structure
The project follows a modular structure, with each key feature broken into manageable components using Django’s best practices.

- `menu/`: Here’s a brief explanation for each component in your Django project structure:

### Project Structure

The project follows a modular structure, with each key feature broken into manageable components using Django’s best practices.

- `menu/`: Manages the cafe menu items and categories, allowing for the addition, modification, and organization of  drink offerings.

- `accounts/`: Handles user account management, including authentication and user-related functionalities.
  - `login/`: Provides a login interface for users to access their accounts.
  - `manager_dashboard/`: Displays an overview and controls for managers to monitor and manage operations.
  - `staff_list/`: Lists all staff members with relevant details for easy management.
  - `update_staff/<int:pk>`: Allows for updating the information of a specific staff member identified by their primary key (pk).
  - `add_staff/`: Provides functionality to add new staff members to the system.
  - `staff_dashboard/`: A personalized dashboard for staff members to view their tasks and reports.
  - `logout/`: Handles user logout functionality.
  - `change_password/`: Allows users to change their account password securely.
  - `export_sales_report/`: Facilitates exporting sales reports for analysis and record-keeping.

- `cart/`: Manages the shopping cart functionality for users to handle their selected items before checkout.
  - `add/<int:product_id>/`: Adds a product to the cart based on the product ID.
  - `remove/<int:product_id>/`: Removes a specific product from the cart using its ID.
  - `finalize/`: Finalizes the cart for checkout, preparing the order for submission.
  - `order_summary/`: Displays a summary of the current order, including items and total cost.
  - `order_history/`: Shows the history of past orders made by the user.
  - `order_detail/<int:order_id>/`: Provides detailed information about a specific order identified by its order ID.
  - `checkout/`: Facilitates the checkout process where users can review and confirm their orders.
  - `update_quantity/<int:product_id>/`: Updates the quantity of a specific product in the cart.

- `site/`: Contains the main website files and templates, serving as the user interface for the cafe's online presence.

- `order/`: Handles customer orders and cart functionality.
  - `create/`: Facilitates the creation of new customer orders.
  - `update/<int:pk>/`: Allows for updating details of an existing order based on its primary key.
  - `delete/<int:pk>/`: Handles the deletion of an order identified by its primary key.
  - `tables/`: Manages the restaurant tables and their statuses for customer seating.
    - `tables/create/`: Enables the creation of new tables within the system.
    - `tables/update/<int:pk>/`: Allows for updating the details of a specific table.
  - `add_product/`: Facilitates adding new products to the menu.
  - `add_category/`: Allows for the creation of new product categories for better organization.
  - `update_product/<int:pk>/`: Enables updating the details of a specific product.
  - `update_category/<int:pk>/`: Allows for updating the details of a specific product category.
  - `popular_products/`: Displays a list of popular products based on sales or customer preferences.
  - `<str:name>/`: Routes to a specific product or category page based on the provided name.
  - `<str:name>/<str:product_name>/`: Routes to a specific product detail page based on both the category name and product name. 

## Testing and Coverage

We have written unit tests for all critical features of the application, ensuring over 95% code coverage. The tests cover various functionalities, including cart operations, order creation, and table management. Each test case is designed to validate specific behaviors and ensure the application behaves as expected.

### How to Run Tests

To run the tests, use the following command in your terminal:

```bash
python manage.py test
```

This command will discover and execute all test cases defined in your Django application. 

### Key Test Cases

1. Cart Functionality:
    - 'Initialization': Tests if the cart initializes correctly.
   - 'Adding Products': Verifies that products can be added to the cart.
   - 'Removing Products': Checks that products can be removed from the cart.
   - 'Updating Quantity': Ensures that the quantity of products in the cart can be updated.

3. Order Creation:
   - 'GET Request': Tests the order creation view to ensure it renders correctly.
   - 'POST Request': Validates the order creation process and checks for successful redirection.

4. Table Management:
   - 'Creating Tables': Tests the table creation view to ensure that new tables can be added correctly.



## Agile Workflow
This project was developed in four weekly sprints, adhering to Agile methodology. Each sprint focused on key features like setup, user authentication, menu implementation, analytics, and thorough testing. A Trello board was used to manage tasks and track progress.

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b new-feature`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin new-feature`.
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
Special thanks to the Product Manager and the instructors for their guidance and support throughout the project.

