
# 🌟 Cafe Shop Adventure: Django Full-Stack Project 🌟

Welcome to the **Cafe Shop Adventure**, a Django full-stack web application designed to manage a cafe's online presence. This project aims to build a fully functional web application for a cafe that includes an online menu for customers, an administrative staff panel, sales analytics, and a rewards system. 

## Features

### Customer-Facing Features:
- **Browse Menu**: Customers can explore cafe menu items by category.
- **Order Placement**: Users can add items to the cart and place orders.
- **Rewards System**: A loyalty program for returning customers.
- **Mobile-Friendly**: Responsive design optimized for mobile devices.

### Staff and Manager Features:
- **Order Management**: Staff can view and manage customer orders.
- **Menu Management**: Admin users can update menu items and categories.
- **Sales Analytics**: Managers have access to key sales metrics, reports, and customer data.

## Tech Stack
- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (with animations and transitions)
- **Version Control**: Git (GitHub repository)

## Setup Instructions

### Prerequisites:
- Python 3.x
- PostgreSQL
- Git

### Installation Steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/cafe-shop-adventure.git
    cd cafe-shop-adventure
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

- `menu/`: Manages the cafe menu items and categories.
- `orders/`: Handles customer orders and cart functionality.
- `staff_panel/`: Provides staff with tools for managing orders and updating the menu.
- `analytics/`: Displays sales metrics and reports to the manager.

## Testing and Coverage
We have written unit tests for all critical features of the application, ensuring over 95% code coverage. To run tests:

```bash
python manage.py test
```

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

