# Docker Setup Guide for Library Management System

This guide will help you run the Library Management System using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose installed (comes with Docker Desktop)

## Step-by-Step Instructions

### Step 1: Verify Docker Installation

```powershell
docker --version
docker-compose --version
```

Both commands should show version numbers.

### Step 2: Create Environment File

The `.envs/.env.dev` file has been created with default values. You can modify it if needed:

```env
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production-12345
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=library_password123
DB_HOST=db
DB_PORT=5432
POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=library_password123
CELERY_BROKER_URL=redis://redis:6379/0
```

**Important Notes:**
- `DB_HOST=db` - This is the Docker service name, not `localhost`
- `CELERY_BROKER_URL=redis://redis:6379/0` - Uses Docker service name `redis`

### Step 3: Build and Start Containers

**Option A: Quick Start (Automated Script)**
```powershell
.\docker-run.ps1
```

**Option B: Manual Start**
```powershell
docker-compose up -d --build
```

This will:
- Build the Docker image
- Create and start all containers (web, db, redis, celery, celery-beat, pgadmin)
- Run database migrations automatically
- Collect static files automatically
- Start the Django server

**Note:** The project uses `config.settings.docker` settings module which reads from `.envs/.env.dev` file.

### Step 4: Check Container Status

```powershell
docker-compose ps
```

You should see all containers running:
- `web` - Django application
- `db` - PostgreSQL database
- `redis` - Redis cache/broker
- `celery` - Celery worker
- `celery-beat` - Celery scheduler
- `pgadmin` - PostgreSQL admin interface

### Step 5: View Logs

To see application logs:

```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Step 6: Access the Application

Once containers are running:

- **API Documentation (Swagger):** http://localhost:8000/api/docs/
- **API Documentation (Redoc):** http://localhost:8000/api/redoc/
- **Django Admin:** http://localhost:8000/admin/
- **pgAdmin:** http://localhost:5050/
  - Email: `admin@admin.com`
  - Password: `123456789`

### Step 7: Create Superuser (Optional)

To create an admin user:

```powershell
docker-compose exec web python manage.py createsuperuser
```

## Common Docker Commands

### Stop Containers
```powershell
docker-compose stop
```

### Stop and Remove Containers
```powershell
docker-compose down
```

### Stop and Remove Containers + Volumes (⚠️ Deletes database data)
```powershell
docker-compose down -v
```

### Restart Containers
```powershell
docker-compose restart
```

### Rebuild After Code Changes
```powershell
docker-compose up -d --build
```

### Run Django Commands
```powershell
# Run migrations
docker-compose exec web python manage.py migrate --settings=config.settings.docker

# Create superuser
docker-compose exec web python manage.py createsuperuser --settings=config.settings.docker

# Django shell
docker-compose exec web python manage.py shell --settings=config.settings.docker

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput --settings=config.settings.docker
```

### Access Container Shell
```powershell
# Web container
docker-compose exec web sh

# Database container
docker-compose exec db psql -U library_user -d library_db
```

## Troubleshooting

### Issue: Port Already in Use

If port 8000, 5432, 6379, or 5050 is already in use:

1. Stop the service using that port, or
2. Modify ports in `docker-compose.yml`:
   ```yaml
   ports:
     - "8001:8000"  # Change host port
   ```

### Issue: Database Connection Failed

- Check that `DB_HOST=db` (Docker service name, not localhost)
- Verify database container is running: `docker-compose ps db`
- Check database logs: `docker-compose logs db`

### Issue: Containers Won't Start

- Check logs: `docker-compose logs`
- Verify `.envs/.env.dev` file exists
- Try rebuilding: `docker-compose up -d --build --force-recreate`

### Issue: Permission Errors

On Linux/Mac, you might need to fix permissions:
```bash
sudo chown -R $USER:$USER .
```

### Issue: Out of Memory

Docker Desktop might need more resources:
1. Open Docker Desktop
2. Go to Settings → Resources
3. Increase Memory allocation

## Database Setup in Docker

The database is automatically created by PostgreSQL container using environment variables:
- `POSTGRES_DB=library_db`
- `POSTGRES_USER=library_user`
- `POSTGRES_PASSWORD=library_password123`

Migrations run automatically when the web container starts.

## Production Setup

For production, use `docker-compose.prod.yml`:

```powershell
docker-compose -f docker-compose.prod.yml up -d --build
```

Make sure to:
1. Create `.envs/.env.prod` with production values
2. Set `DEBUG=False`
3. Use a strong `SECRET_KEY`
4. Configure proper `ALLOWED_HOSTS`

## Summary

✅ **Quick Start:**
```powershell
docker-compose up -d --build
```

✅ **Access:**
- API: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/
- pgAdmin: http://localhost:5050/

✅ **Stop:**
```powershell
docker-compose down
```

