-- PostgreSQL Setup Queries for Library Management System
-- Run these queries one by one in PostgreSQL (using psql or pgAdmin)

-- Step 1: Create a new user (role) for the library management system
-- Change 'library_user' and 'library_password123' to your preferred values
CREATE USER library_user WITH PASSWORD 'library_password123';

-- Step 2: Grant the user permission to create databases
ALTER USER library_user CREATEDB;

-- Step 3: Create the database
CREATE DATABASE library_db OWNER library_user;

-- Step 4: Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;

-- Step 5: Connect to the new database (run this command separately)
-- \c library_db

-- Step 6: Grant schema privileges (required for PostgreSQL 15+)
-- Run this AFTER connecting to library_db (after \c library_db)
GRANT ALL ON SCHEMA public TO library_user;

-- Step 7: Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO library_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO library_user;

-- Verification queries (optional - to check everything was created):
-- List all users:
-- \du library_user

-- List all databases:
-- \l library_db

-- Connect to your database:
-- \c library_db

-- List tables (after running Django migrations):
-- \dt


