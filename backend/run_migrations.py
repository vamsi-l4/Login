import os
import django
from django.core.management import call_command

def migrate():
    """Run database migrations."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_backend.settings')
    django.setup()
    print("Starting database migration...")
    call_command('migrate')
    print("Database migration completed successfully.")

if __name__ == '__main__':
    migrate()
