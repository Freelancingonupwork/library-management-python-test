# Library Management System

A comprehensive library management system built with Django and Django REST Framework, featuring both RESTful API endpoints and user-friendly HTML interfaces.

## Features

### Authentication & User Management
- ✅ User registration and login with HTML pages (`/account/login`, `/account/register`)
- ✅ JWT-based authentication for API access
- ✅ Role-based access control (Admin, Librarian, Member)
- ✅ Member self-registration with automatic account creation

### Book Management
- ✅ User-friendly HTML book browsing interface (`/library/books/`)
- ✅ Search books by title, ISBN, author, or subject
- ✅ Filter books by author and subject
- ✅ Book detail pages with availability information
- ✅ Adding new Authors and Books by librarians and admins
- ✅ Book availability tracking (Available, Borrowed, Reserved, Lost)
- ✅ Multiple copies support with barcode tracking

### Borrowing System
- ✅ Members can borrow books directly from the web interface
- ✅ Automatic due date calculation (14 days default)
- ✅ Borrowing history tracking
- ✅ Duplicate borrow prevention
- ✅ Automatic book status updates

### API & Documentation
- ✅ RESTful API endpoints for all features
- ✅ OpenAPI/Swagger documentation (`/api/docs`)

### Production Ready
- ✅ Docker and Docker Compose support
- ✅ PostgreSQL database support
- ✅ Static files configuration
- ✅ Gunicorn WSGI server configuration
- ✅ Celery for background tasks
- ✅ Redis for task queue
- ✅ Modular design
- ✅ Cloud-native 12-factor methodology

## Apps

The project consists of 4 Django apps:

- 🔋 **`core`**: Core models and abstract features used throughout the project
- 🔋 **`accounts`**: User authentication, member and librarian management
- 🔋 **`library`**: Book and author management, HTML views for browsing
- 🔋 **`borrowing`**: Book borrowing functionality and records

## Technologies Used

- ✨ [Python](https://www.python.org/) - Programming Language
- ✨ [Django](https://docs.djangoproject.com/) - Web Framework
- ✨ [Django REST Framework](https://www.django-rest-framework.org/) - RESTful API Framework
- ✨ [Docker](https://www.docker.com/) - Container Platform
- ✨ [PostgreSQL](https://www.postgresql.org/) - Database
- ✨ [Redis](https://redis.io/) - Task Queue & Caching
- ✨ [Celery](https://github.com/celery/celery) - Distributed Task Queue
- ✨ [Celery Beat](https://github.com/celery/django-celery-beat) - Task Scheduler
- ✨ [Gunicorn](https://gunicorn.org/) - WSGI HTTP Server
- ✨ [drf-spectacular](https://github.com/tfranzel/drf-spectacular) - OpenAPI 3 schema generation

## Installation

### Prerequisites

- Python 3.7+
- PostgreSQL (or use Docker)
- Docker & Docker Compose (optional, for containerized setup)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd library-management-main
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create `.envs/.env` file:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=library_db
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Set up PostgreSQL database**
   
   Create database and user:
   ```sql
   CREATE USER library_user WITH PASSWORD 'your_password';
   ALTER USER library_user CREATEDB;
   CREATE DATABASE library_db OWNER library_user;
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

   Access the application at `http://localhost:8000`

### Docker Setup

For detailed Docker setup instructions, refer to:
- **`DOCKER_SETUP.md`** - Complete step-by-step Docker setup guide
- **`DOCKER_QUICK_START.md`** - Quick reference for Docker setup
- **`DOCKER_POSTGRESQL_ACCESS.md`** - PostgreSQL database access guide

#### Quick Docker Setup

1. **Prerequisites**
   - Docker Desktop installed and running
   - Docker Compose (included with Docker Desktop)

2. **Configuration Files**
   
   The following files are used for Docker setup:
   - **`docker-compose.yml`** - Docker Compose configuration (defines all services)
   - **`Dockerfile`** - Docker image build instructions
   - **`.envs/.env.dev`** - Environment variables for Docker development
   - **`config/settings/docker.py`** - Django settings for Docker environment
   - **`docker-run.ps1`** - PowerShell script for automated Docker setup (Windows)

3. **Set up environment file**
   
   Create or edit `.envs/.env.dev` with your configuration:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here-change-in-production
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web
   DB_NAME=library_db
   DB_USER=library_user
   DB_PASSWORD=library_password
   DB_HOST=db
   DB_PORT=5432
   ```

4. **Run with Docker Compose**

   **Option A: Using PowerShell script (Windows)**
   ```powershell
   .\docker-run.ps1
   ```

   **Option B: Manual Docker Compose command**
   ```bash
   docker-compose up -d --build
   ```

   This will start 7 containers:
   - `web` - Django application server
   - `db` - PostgreSQL database
   - `pgadmin` - PostgreSQL admin interface (port 5050)
   - `redis` - Redis server for Celery
   - `celery` - Celery worker for background tasks
   - `celery-beat` - Celery scheduler for periodic tasks

5. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate --settings=config.settings.docker
   ```

6. **Create superuser** (optional)
   ```bash
   docker-compose exec web python manage.py createsuperuser --settings=config.settings.docker
   ```

7. **Access the application**
   - Main Application: `http://localhost:8000`
   - pgAdmin: `http://localhost:5050`
   - API Docs: `http://localhost:8000/api/docs`

#### Docker Services Overview

| Service | Port | Description |
|---------|------|-------------|
| web | 8000 | Django application |
| db | 5432 | PostgreSQL database |
| pgadmin | 5050 | PostgreSQL admin interface |
| redis | 6379 | Redis server (internal) |

#### Useful Docker Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f web

# Stop all containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild containers
docker-compose up -d --build

# Execute commands in web container
docker-compose exec web python manage.py <command>

# Access database shell
docker-compose exec db psql -U library_user -d library_db
```

#### Docker Configuration Files Reference

- **`docker-compose.yml`**: Defines all services (web, db, redis, celery, etc.)
- **`Dockerfile`**: Builds the Python/Django application image
- **`.envs/.env.dev`**: Environment variables for Docker development
- **`config/settings/docker.py`**: Django settings module for Docker
- **`docker-run.ps1`**: Automated setup script for Windows PowerShell

## Access Points

### Web Interface
- **Main Application**: `http://localhost:8000` (or `http://0.0.0.0:8000` in Docker)
- **Login Page**: `http://localhost:8000/account/login`
- **Registration Page**: `http://localhost:8000/accounts/register/`
- **Books List**: `http://localhost:8000/library/books/`
- **Django Admin**: `http://localhost:8000/admin/`

### API Documentation
- **Swagger UI**: `http://localhost:8000/api/docs`
- **Redoc**: `http://localhost:8000/api/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### Docker Services
- **pgAdmin**: `http://localhost:5050` (when using Docker)

## User Roles

### Admin
- Full system access
- Manage all books, authors, and users
- View all borrowing records

### Librarian
- Add/edit books and authors
- View all borrowing records
- Process book returns

### Member
- Browse books (HTML interface)
- Borrow books directly
- View personal borrowing history
- Register new account

## Project Structure

```
library-management-main/
├── accounts/          # User authentication and management
├── borrowing/         # Book borrowing functionality
├── config/           # Django settings and configuration
├── core/             # Core models and utilities
├── fines/            # Fine calculation and management
├── library/          # Book and author management
├── reservation/      # Book reservation system
├── static/           # Static files (CSS, JS)
├── templates/        # HTML templates
├── .envs/            # Environment configuration files
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile        # Docker image definition
├── manage.py         # Django management script
├── pyproject.toml    # Poetry dependencies
└── requirements.txt  # Python dependencies
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Formatting
```bash
black .
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## License

MIT License

Copyright (c) 2025
