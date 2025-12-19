# Docker Quick Start Guide

## ✅ Project Configuration Status

The project is **correctly configured** to run in Docker! Here's what has been set up:

### Files Created/Updated:
- ✅ `config/settings/docker.py` - Docker-specific settings
- ✅ `.envs/.env.dev` - Environment variables for Docker
- ✅ `docker-compose.yml` - Updated to use docker settings
- ✅ `docker-run.ps1` - Quick start script
- ✅ `DOCKER_SETUP.md` - Complete setup guide

## 🚀 Quick Start (3 Steps)

### Step 1: Ensure Docker Desktop is Running
Make sure Docker Desktop is installed and running on your machine.

### Step 2: Run the Quick Start Script
```powershell
.\docker-run.ps1
```

**OR** manually run:
```powershell
docker-compose up -d --build
```

### Step 3: Access the Application
Wait ~30 seconds for services to start, then access:

- **API Docs:** http://localhost:8000/api/docs/
- **Admin Panel:** http://localhost:8000/admin/
- **pgAdmin:** http://localhost:5050/ (admin@admin.com / 123456789)

## 📋 What Gets Created

Docker will create and start these containers:

1. **web** - Django application server
2. **db** - PostgreSQL database (auto-creates database and user)
3. **redis** - Redis cache/broker for Celery
4. **celery** - Celery worker for background tasks
5. **celery-beat** - Celery scheduler for periodic tasks
6. **pgadmin** - PostgreSQL administration interface

## 🔧 Key Configuration Details

### Database Connection
- **Host:** `db` (Docker service name, not localhost)
- **Database:** `library_db` (auto-created)
- **User:** `library_user` (auto-created)
- **Password:** `library_password123`

### Environment Variables
All configured in `.envs/.env.dev`:
- `DB_HOST=db` ← Important: Uses Docker service name
- `CELERY_BROKER_URL=redis://redis:6379/0` ← Uses Docker service name

### Settings Module
Docker uses `config.settings.docker` which:
- Reads from `.envs/.env.dev`
- Connects to PostgreSQL at `db` host
- Connects to Redis at `redis` host

## 📝 Common Commands

```powershell
# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f web

# Stop containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Restart containers
docker-compose restart

# Create superuser
docker-compose exec web python manage.py createsuperuser --settings=config.settings.docker

# Run migrations manually
docker-compose exec web python manage.py migrate --settings=config.settings.docker

# Access Django shell
docker-compose exec web python manage.py shell --settings=config.settings.docker
```

## ✅ Verification Checklist

After running `docker-compose up -d --build`:

- [ ] All containers are running: `docker-compose ps`
- [ ] No errors in logs: `docker-compose logs`
- [ ] API docs accessible: http://localhost:8000/api/docs/
- [ ] Database connected (check web container logs)
- [ ] Migrations applied (check web container logs)

## 🐛 Troubleshooting

### Port Already in Use
If ports 8000, 5432, 6379, or 5050 are in use:
- Stop the service using that port, OR
- Modify ports in `docker-compose.yml`

### Database Connection Failed
- Check `DB_HOST=db` in `.envs/.env.dev`
- Verify database container is running: `docker-compose ps db`
- Check logs: `docker-compose logs db`

### Containers Won't Start
- Check Docker Desktop is running
- Check logs: `docker-compose logs`
- Try: `docker-compose down` then `docker-compose up -d --build`

## 📚 Full Documentation

See `DOCKER_SETUP.md` for complete documentation.

