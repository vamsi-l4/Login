#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_backend.settings')

# Setup Django
django.setup()

# Run migrations
try:
    print("Starting database migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("Migrations completed successfully!")
except Exception as e:
    print(f"Migration failed: {e}")
    sys.exit(1)
