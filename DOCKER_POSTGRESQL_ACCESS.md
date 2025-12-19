# Access Docker PostgreSQL from Local Machine

## Connection Details

**Host:** `localhost` (or `127.0.0.1`)  
**Port:** `5432`  
**Database:** `library_db`  
**Username:** `library_user`  
**Password:** `library_password123`

## Method 1: Using psql Command Line

### Connect to PostgreSQL:
```powershell
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5432 -U library_user -d library_db
```

Or if psql is in your PATH:
```powershell
psql -h localhost -p 5432 -U library_user -d library_db
```

### Common psql Commands:
```sql
-- List all databases
\l

-- List all tables
\dt

-- Describe a table
\d table_name

-- Run SQL query
SELECT * FROM library_book LIMIT 10;

-- Exit
\q
```

## Method 2: Using pgAdmin (Web Interface)

1. **Access pgAdmin:** http://localhost:5050/
   - Email: `admin@admin.com`
   - Password: `123456789`

2. **Add Server:**
   - Right-click "Servers" → "Create" → "Server"
   - **General Tab:**
     - Name: `Docker PostgreSQL`
   - **Connection Tab:**
     - Host name/address: `db` (Docker service name) or `host.docker.internal` if accessing from host
     - Port: `5432`
     - Maintenance database: `library_db`
     - Username: `library_user`
     - Password: `library_password123`
   - Click "Save"

**Note:** If connecting from pgAdmin running on your host machine, you might need to use `host.docker.internal` instead of `db`.

## Method 3: Using Docker Exec

Access PostgreSQL directly from Docker container:

```powershell
# Connect to database
docker-compose exec db psql -U library_user -d library_db

# Run SQL commands
docker-compose exec db psql -U library_user -d library_db -c "SELECT version();"

# List tables
docker-compose exec db psql -U library_user -d library_db -c "\dt"
```

## Method 4: Using Python Script

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="library_db",
    user="library_user",
    password="library_password123"
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
conn.close()
```

## Method 5: Using Database GUI Tools

### DBeaver / DataGrip / TablePlus:
- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `library_db`
- **Username:** `library_user`
- **Password:** `library_password123`

## Troubleshooting

### Issue: "Connection refused" or "Connection timeout"
- **Solution:** Make sure Docker containers are running:
  ```powershell
  docker-compose ps
  ```
- Check if port 5432 is exposed:
  ```powershell
  docker-compose ps db
  ```

### Issue: "Password authentication failed"
- **Solution:** Verify credentials in `.envs/.env.dev`:
  ```
  POSTGRES_USER=library_user
  POSTGRES_PASSWORD=library_password123
  DB_PASSWORD=library_password123
  ```

### Issue: "Database does not exist"
- **Solution:** Database is auto-created, but you can verify:
  ```powershell
  docker-compose exec db psql -U library_user -c "\l"
  ```

### Issue: Port 5432 already in use
- **Solution:** Your local PostgreSQL might be using port 5432. Options:
  1. Stop local PostgreSQL service
  2. Change Docker PostgreSQL port in `docker-compose.yml`:
     ```yaml
     ports:
       - "5433:5432"  # Use 5433 on host
     ```

## Quick Connection Test

Test connection from PowerShell:
```powershell
$env:PGPASSWORD='library_password123'
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5432 -U library_user -d library_db -c "SELECT version();"
Remove-Item Env:\PGPASSWORD
```

## Summary

✅ **Easiest Method:** Use pgAdmin at http://localhost:5050/  
✅ **Command Line:** Use psql from your local PostgreSQL installation  
✅ **From Host:** Connect to `localhost:5432`  
✅ **From Docker:** Use `docker-compose exec db psql`

