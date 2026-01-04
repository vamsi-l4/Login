#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # HACK: Running migrations programmatically because of execution restrictions.
    # This should be removed after the first successful run.
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        django.setup()
        from django.core.management import call_command
        print("---------- HACK: Applying database migrations... ----------")
        call_command('migrate')
        print("---------- HACK: Migrations applied. --------------------")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
