🍔 Fast Food Backend API
A robust and scalable RESTful API for a fast food ordering system, built with Python Flask, PostgreSQL, and JWT authentication. This backend supports full menu management, order processing, user authentication, and image uploads.

https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Flask-2.3.3-green
https://img.shields.io/badge/PostgreSQL-15%252B-blue
https://img.shields.io/badge/JWT-Authentication-orange

✨ Features
🔐 JWT Authentication – Secure user registration, login, and role-based access

📦 Menu Management – Full CRUD operations for categories and food items

🛒 Order System – Complete order lifecycle (pending, preparing, ready, completed)

🌐 Cloudinary Integration – Efficient image upload and management for menu items

🚀 PostgreSQL with Neon – Serverless, scalable database solution

📚 Well-Documented API – Clear endpoints with request/response examples

⚡ Flask & Python – Lightweight and efficient backend framework

🚀 Quick Start
Prerequisites
Python 3.8+

PostgreSQL database (or Neon account)

Cloudinary account (for image storage)

1. Clone the Repository
bash
git clone https://github.com/awash-dev/fast-food-backend.git
cd fast-food-backend
2. Set Up Virtual Environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Environment Configuration
Create a .env file in the root directory:

env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
NEON_DATABASE_URL=your-neon-database-connection-string
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
5. Database Setup
bash
flask db init
flask db migrate
flask db upgrade
6. Run the Application
bash
flask run
The API will be available at http://localhost:5000

📁 Project Structure
text
fast-food-backend/
├── app/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── routes.py          # API routes
│   ├── auth.py            # Authentication functions
│   └── uploads.py         # Image upload handling
├── migrations/            # Database migration files
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
├── config.py              # Application configuration
└── run.py                 # Application entry point
🗂️ API Endpoints
Authentication Endpoints
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	User login
POST	/auth/logout	User logout
GET	/auth/profile	Get user profile
Menu Endpoints
Method	Endpoint	Description	Access
GET	/menu	Get all menu items	Public
GET	/menu/<id>	Get specific menu item	Public
POST	/menu	Create new menu item	Admin
PUT	/menu/<id>	Update menu item	Admin
DELETE	/menu/<id>	Delete menu item	Admin
Category Endpoints
Method	Endpoint	Description	Access
GET	/categories	Get all categories	Public
POST	/categories	Create new category	Admin
Order Endpoints
Method	Endpoint	Description	Access
GET	/orders	Get user's orders	User
POST	/orders	Create new order	User
GET	/orders/<id>	Get specific order	User/Admin
PUT	/orders/<id>	Update order status	Admin
Upload Endpoints
Method	Endpoint	Description	Access
POST	/upload	Upload image to Cloudinary	Admin
🗄️ Database Schema
Users Table
id (Primary Key)

username (String, Unique)

email (String, Unique)

password_hash (String)

role (String: 'customer' or 'admin')

created_at (DateTime)

MenuItems Table
id (Primary Key)

name (String)

description (Text)

price (Float)

image_url (String)

category_id (Foreign Key to Categories)

is_available (Boolean)

Categories Table
id (Primary Key)

name (String, Unique)

description (Text)

Orders Table
id (Primary Key)

user_id (Foreign Key to Users)

status (String: 'pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled')

total_amount (Float)

created_at (DateTime)

updated_at (DateTime)

OrderItems Table
id (Primary Key)

order_id (Foreign Key to Orders)

menu_item_id (Foreign Key to MenuItems)

quantity (Integer)

price_at_time (Float)

🔐 Authentication
The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

text
Authorization: Bearer <your-jwt-token>
Example Registration Request
bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
Example Login Request
bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
🧪 Testing
Run the test suite with:

bash
python -m pytest tests/
🚀 Deployment
Production Deployment with Gunicorn
Install Gunicorn:

bash
pip install gunicorn
Run with Gunicorn:

bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
Environment Variables for Production
Set these additional variables in your production environment:

env
FLASK_ENV=production
DEBUG=False
🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature-name

Commit your changes: git commit -m 'Add feature'

Push to the branch: `git push origin
 
