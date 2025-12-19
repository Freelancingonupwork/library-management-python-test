# Quick Docker Setup Script for Windows
# Run this script to start the Library Management System in Docker

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker Setup for Library Management" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Docker installation
Write-Host "[1/4] Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    $composeVersion = docker-compose --version 2>&1
    Write-Host "[OK] Docker found: $dockerVersion" -ForegroundColor Green
    Write-Host "[OK] Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker not found! Please install Docker Desktop." -ForegroundColor Red
    Write-Host "  Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if Docker is running
Write-Host ""
Write-Host "[2/4] Checking if Docker is running..." -ForegroundColor Yellow
try {
    docker ps 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Docker is running" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Docker is not running. Please start Docker Desktop." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[ERROR] Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check environment file
Write-Host ""
Write-Host "[3/4] Checking environment file..." -ForegroundColor Yellow
if (Test-Path ".envs\.env.dev") {
    Write-Host "[OK] Environment file found" -ForegroundColor Green
} else {
    Write-Host "[INFO] .envs/.env.dev not found! Creating it..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path ".envs" | Out-Null
    $envContent = "DEBUG=True`n"
    $envContent += "SECRET_KEY=django-insecure-dev-key-change-in-production-12345`n"
    $envContent += "ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web`n"
    $envContent += "DB_NAME=library_db`n"
    $envContent += "DB_USER=library_user`n"
    $envContent += "DB_PASSWORD=library_password123`n"
    $envContent += "DB_HOST=db`n"
    $envContent += "DB_PORT=5432`n"
    $envContent += "POSTGRES_DB=library_db`n"
    $envContent += "POSTGRES_USER=library_user`n"
    $envContent += "POSTGRES_PASSWORD=library_password123`n"
    $envContent += "CELERY_BROKER_URL=redis://redis:6379/0"
    $envContent | Out-File -FilePath ".envs\.env.dev" -Encoding ASCII -NoNewline
    Write-Host "[OK] Created .envs/.env.dev" -ForegroundColor Green
}

# Build and start containers
Write-Host ""
Write-Host "[4/4] Building and starting Docker containers..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Gray
Write-Host ""

docker-compose up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    Write-Host ""
    Write-Host "Access your application:" -ForegroundColor Cyan
    Write-Host "  - API Documentation: http://localhost:8000/api/docs/" -ForegroundColor White
    Write-Host "  - Admin Panel: http://localhost:8000/admin/" -ForegroundColor White
    Write-Host "  - pgAdmin: http://localhost:5050/" -ForegroundColor White
    Write-Host "    (Email: admin@admin.com, Password: 123456789)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Cyan
    Write-Host "  - View logs: docker-compose logs -f" -ForegroundColor White
    Write-Host "  - Stop: docker-compose stop" -ForegroundColor White
    Write-Host "  - Stop and remove: docker-compose down" -ForegroundColor White
    Write-Host "  - Create superuser: docker-compose exec web python manage.py createsuperuser --settings=config.settings.docker" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "[ERROR] Setup failed. Check the error above." -ForegroundColor Red
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  - Ports already in use (8000, 5432, 6379, 5050)" -ForegroundColor White
    Write-Host "  - Docker Desktop not running" -ForegroundColor White
    Write-Host "  - Insufficient disk space" -ForegroundColor White
}
