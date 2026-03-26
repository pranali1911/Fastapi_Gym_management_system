Gym Management System
📌 Project Overview

The Gym Management System is a backend application built using FastAPI designed to manage membership plans, handle enrollments, and support class booking workflows.

This project demonstrates core backend engineering concepts, including:

RESTful API design
Pydantic validation
CRUD operations
Multi-step workflows (enrollment → booking → management)
Search, sorting, and pagination
🛠️ Technologies Used
Technology	Purpose
Python	Core programming language
FastAPI	Backend API framework
Pydantic	Data validation
Uvicorn	ASGI server
Swagger UI	API testing
⚙️ Project Architecture & Features
🔹 Route Optimization

All fixed routes (/plans/search, /plans/filter, etc.) are placed above variable routes (/plans/{plan_id}) to ensure correct request handling.

🔹 Multi-Step Workflow

Enroll → Book Class → Manage Membership

Enroll member → creates active membership
Book class → allowed only if plan includes classes
Cancel booking
Freeze membership
Reactivate membership
🔹 Advanced Features
🔍 Search (plan name, case-insensitive)
🔄 Sorting (price, duration, name)
📄 Pagination (page, limit)
🔗 Combined /browse endpoint
📂 Project Structure
Fastapi_Gym_management_system/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── output/
⚡ Installation & Setup
1. Create Virtual Environment
python -m venv venv
2. Activate Environment
Windows
venv\Scripts\activate
Mac/Linux
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Run Server
uvicorn main:app --reload
5. Open Swagger
http://127.0.0.1:8000/docs
📡 API Summary
🔹 Basic
GET /
GET /plans
GET /plans/{plan_id}
GET /plans/summary
GET /memberships
🔹 Discovery
GET /plans/search
GET /plans/sort
GET /plans/page
GET /plans/browse
GET /plans/filter
🔹 Workflow
POST /memberships
POST /classes/book
GET /classes/bookings
DELETE /classes/cancel/{booking_id}
PUT /memberships/{id}/freeze
PUT /memberships/{id}/reactivate
🔹 CRUD
POST /plans
PUT /plans/{plan_id}
DELETE /plans/{plan_id}
💰 Membership Fee Logic

The system calculates membership fees with:

6+ months → 10% discount
12+ months → 20% discount
EMI payment → ₹200 processing fee
Referral code → additional 5% discount
📸 Screenshots

All endpoints (Q1–Q20) are tested.

Located in:

/output

Includes:

Success responses
Error handling
Validation cases
Swagger UI testing
🧪 Testing

Swagger UI:

http://127.0.0.1:8000/docs

All APIs are tested using Swagger.

🎯 Learning Outcomes
FastAPI backend development
API design and routing
Request validation using Pydantic
Business logic implementation
CRUD operations
Multi-step workflows
Search, sorting, pagination
GitHub project management
🙏 Acknowledgement

Developed as part of the FastAPI Internship at Innomatics Research Labs.

⭐ Thank you for reviewing this project!
