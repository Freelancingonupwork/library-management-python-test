#!/usr/bin/env python
"""Check database tables and create if needed"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection

# Check existing tables
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    tables = [row[0] for row in cursor.fetchall()]

print(f"\n{'='*60}")
print(f"Current tables in database: {len(tables)}")
print(f"{'='*60}")

if tables:
    print("\nExisting tables:")
    for table in tables:
        print(f"  ✓ {table}")
else:
    print("\n⚠ No tables found in database!")
    print("Running migrations to create tables...")
    print("\n" + "="*60)

