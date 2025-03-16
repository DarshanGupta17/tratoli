# Django Task Management API

## Overview
This is a Django-based task management system that provides JWT authentication, task management features, report generation, real-time updates, and more. The project includes features like:
- **JWT-based authentication** (Django REST Framework)
- **Task CRUD operations** (with filtering & pagination)
- **Multi-threaded report generation**
- **Asynchronous notifications** (Celery & Redis)
- **Caching using Redis**
- **WebSocket real-time updates** (Django Channels)
- **Rate Limiting** (DRF throttling)
- **Task export as CSV (async via Celery)**

---

## Tech Stack
- **Backend:** Django, Django REST Framework, Celery, Redis
- **Database:** PostgreSQL / MySQL
- **Caching & Messaging:** Redis
- **Asynchronous Task Processing:** Celery
- **Real-time Updates:** Django Channels & WebSockets

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/tratoli.git
cd tratoli
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file:
``` sample env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*

USE_POSTGRES=True
DB_NAME=tratoli
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432

CELERY_BROKER_URL=redis://127.0.0.1:6379
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379

EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Start Redis Server
```bash
redis-server
```

### 8. Start Celery Worker
```bash
celery -A TMS worker --loglevel=info
```

### 9. Run Django Development Server
```bash
python manage.py runserver
```

---

## API Endpoints

### **Authentication**
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Get JWT token
- `GET /api/auth/profile/` - View user profile

### **Task Management**
- `GET /api/tasks/` - List tasks (supports pagination & filtering)
- `POST /api/tasks/` - Create a task
- `GET /api/tasks/?task_id=pk` - Retrieve a task
- `PUT /api/tasks/?task_id=pk` - Update a task
- `DELETE /api/tasks/?task_id=pk` - Delete a task

### **Task Export (Async CSV)**
- `POST /api/tasks/export/` - Start CSV export (email sent when ready)

### **Reports & Analytics**
- `GET /api/tasks/report/` - Get task summary (multi-threaded)


### **WebSocket (Real-Time Updates)**
- Connect to: `ws://localhost:8000/ws/tasks/`

---

## Caching (Redis)
- Task list API responses are cached for **60 seconds**.
- Reports API responses are cached for **5 minutes**.
- Cache is **automatically cleared** when tasks are updated.

---

## Rate Limiting
- **Authenticated users**: 100 requests/hour
- **Anonymous users**: 10 requests/minute


## Deployment
### Using Docker
```bash
docker-compose up --build
```

### Production Setup
- Use **Gunicorn** and **Daphne** for ASGI
- Use **Celery Beat** for periodic tasks
- Use **Nginx & Gunicorn** for reverse proxy


