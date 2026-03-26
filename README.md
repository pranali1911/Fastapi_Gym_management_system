# 🏋️ Gym Management System

## 📌 Project Overview
The Gym Management System is a backend application built using FastAPI designed to manage membership plans, handle enrollments, and support class booking workflows.

This project demonstrates core backend engineering concepts, including:

- RESTful API design  
- Pydantic data validation  
- CRUD operations  
- Multi-step workflows (enrollment → booking → management)  
- Search, sorting, and pagination  

---

## 🛠️ Technologies Used

| Technology | Purpose |
|----------|--------|
| Python | Core programming language |
| FastAPI | Backend API framework |
| Pydantic | Data validation |
| Uvicorn | ASGI server |
| Swagger UI | API testing |

---

## ⚙️ Project Architecture & Features

### 🔹 Route Optimization
All fixed routes (/plans/search, /plans/filter, etc.) are placed above variable routes (/plans/{plan_id}) to ensure correct request handling.

---

### 🔹 Multi-Step Workflow
Enroll → Book Class → Manage Membership

- Enroll member → creates active membership  
- Book class → allowed only if plan includes classes  
- Cancel booking  
- Freeze membership  
- Reactivate membership  

---

### 🔹 Advanced Features

- 🔍 Search (plan name, case-insensitive)  
- 🔄 Sorting (price, duration, name)  
- 📄 Pagination (page, limit)  
- 🔗 Combined /browse endpoint  

---

## 📂 Project Structure

```text
Fastapi_Gym_management_system/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── output/
