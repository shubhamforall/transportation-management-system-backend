🚚 Transportation Management System (TMS)
The Transportation Management System (TMS) is a backend API built using Django and Django Rest Framework to streamline transportation workflows. It handles user management, customer tracking, vehicle records, invoicing, and payment processing. The project is structured for clean scalability, consistent API design, and easy deployment using Docker.

✅ Features
🔐 User Authentication (JWT-based)

👥 Customer Management – Create, view, and update customer records

🚛 Vehicle Management – Track vehicles and assign them to customers

🧾 Invoice Module – Generate and manage invoices for customer trips

💵 Payment Module – Record and verify invoice payments

🔔 Notification System – In-app notifications with read/unread tracking

📄 Auto-generated Swagger Docs – Clear, interactive API reference

🐳 Dockerized Setup – Simplified deployment using a Dockerfile and run.sh script

🧰 Tech Stack
Python 3.12+

Django 4.x

Django Rest Framework

SQLite (can be swapped with Postgres/MySQL)

JWT for token authentication

Docker

drf-spectacular for OpenAPI/Swagger generation

🚀 Getting Started (Docker)
🐳 This project includes a Dockerfile for quick containerized deployment. It runs your app using a custom run.sh script and serves on port 8000.

📦 Steps to Run:
bash
Copy
Edit
# 1️⃣ Build the Docker image
docker build -t tms-app .

# 2️⃣ Run the container
docker run -d -p 8000:8000 --name tms-container tms-app

# 3️⃣ (Optional) Enter the running container
docker exec -it tms-container bash

# 4️⃣ Run migrations inside container
python manage.py migrate

# 5️⃣ Create superuser (optional)
python manage.py createsuperuser
✅ Make sure your run.sh file handles collectstatic, migrate, or gunicorn/manage.py runserver as needed.

📚 API Modules Overview
Module	Endpoint Prefix	Description
👤 User/Auth	/api/auth/	Login/logout, token-based access
👥 Customer	/api/customer/	Manage customer records
🚛 Vehicle	/api/vehicle/	Add/update vehicles
🧾 Invoice	/api/invoice/	Create and track invoices
💳 Payment	/api/payment/	Process and validate invoice payments
🔔 Notification	/api/notification/	View and mark notifications as read

📘 API Documentation
Interactive API docs are auto-generated using drf-spectacular.

Tool	URL
🔍 Swagger UI	http://localhost:8000/api/docs
📘 ReDoc	http://localhost:8000/api/redoc
📄 OpenAPI	http://localhost:8000/api/schema

🧪 Testing
bash
Copy
Edit
# Run tests inside container or local environment
python manage.py test
🛠️ Versioning
Use the custom version command to bump and check application version:

bash
Copy
Edit
python manage.py ver MJ  # Major
python manage.py ver MN  # Minor
python manage.py ver BF  # Bug Fix
python manage.py ver CV  # Current Version
📦 Postman Collection
A ready-to-use Postman collection is available for testing APIs.

Collection: postman/TMS_collection.json

Environment: postman/TMS_environment.json

🧑‍💻 Author
Shubham Patil