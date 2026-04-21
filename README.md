# 🚀 TaskFlow – Project & Task Management API

TaskFlow is a backend API built with **Django REST Framework (DRF)** to manage projects and tasks in a structured way using **role-based access control (RBAC)**.

It simulates a real-world workflow where:
- A **CTO** creates projects  
- A **Manager** manages tasks within those projects  
- An **Employee** works only on assigned tasks  

---

## 🛠 Tech Stack

- **Backend:** Django + Django REST Framework  
- **Database:** SQLite (default) / PostgreSQL (production-ready)  
- **Authentication:** Django Auth (Users & Groups)  
- **API Docs:** drf-spectacular (Swagger / OpenAPI)  

---

## 🔒 Roles & Permissions

### 👤 CTO
- Full access to the system  
- Can create projects  
- Can assign managers  
- Can view all tasks  

---

### 👨‍💼 Manager
- Can see **only projects assigned to them**  
- Can create and manage tasks in their projects  
- Cannot create projects  

---

### 👨‍💻 Employee
- Can see **only tasks assigned to them**  
- Can update:
  - Task status  
  - Task notes  
- Cannot create tasks or view projects  

---

## ⚙️ How Security Works

TaskFlow enforces security at multiple levels:

### 1. Query Filtering (Backend Protection)
Each API filters data based on the logged-in user:

- Managers → only their projects  
- Employees → only their tasks  

---

### 2. Serializer Restrictions
- Employees can only update limited fields (`status`, `employee_notes`)  
- Project creator (`created_by`) is automatically set (not editable)  

---

### 3. Dynamic Data Control
- Task creation dropdown shows only:
  - Manager’s own projects  
  - Employees as assignees  

---

## 📂 API Endpoints

### 📁 Tasks

| Method | Endpoint | Description |
|--------|--------|------------|
| GET | `/tasks/api/` | Get tasks (filtered by role) |
| POST | `/tasks/api/` | Create task (CTO / Manager) |
| GET | `/tasks/api/<id>/` | Get single task |
| PATCH | `/tasks/api/<id>/` | Update task (Employee limited) |

---

### 📁 Projects

| Method | Endpoint | Description |
|--------|--------|------------|
| GET | `/tasks/projects/api/` | Get projects |
| POST | `/tasks/projects/api/` | Create project (CTO only) |
| GET | `/tasks/projects/api/<id>/` | Get project details |
| DELETE | `/tasks/projects/api/<id>/` | Delete project (CTO only) |

---

### 👤 Authentication

| Method | Endpoint | Description |
|--------|--------|------------|
| POST | `/tasks/register/` | Register new user |

---

## 📖 API Documentation

Swagger/OpenAPI docs are available via:

- `/api/docs/` (if configured)
- `/api/schema/`

---

## 🎯 Key Features

- Role-Based Access Control (RBAC)
- Secure API (backend-enforced rules)
- Clean project-task relationship
- Dynamic serializer behavior
- Prevents unauthorized data access

---

## ⚙️ Installation

```bash
git clone <your-repo-url>
cd taskflow
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver