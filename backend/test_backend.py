#!/usr/bin/env python
"""
Comprehensive test suite to verify the Django backend is working correctly
"""
import os
import django
import subprocess
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_backend.settings')
django.setup()

from django.core.management import call_command
from io import StringIO

def test_imports():
    """Test if all critical imports work"""
    try:
        from accounts.views import protected_view, clerk_client
        from accounts.models import UserProfile
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_system_check():
    """Test Django system checks"""
    try:
        out = StringIO()
        call_command('check', stdout=out)
        print("✓ Django system check passed")
        return True
    except Exception as e:
        print(f"✗ Django check failed: {e}")
        return False

def test_clerk_client():
    """Test Clerk client initialization"""
    try:
        from accounts.views import clerk_client
        from clerk import Clerk
        if clerk_client is None:
            print("⚠ Clerk client is None (CLERK_SECRET_KEY might not be set)")
        elif isinstance(clerk_client, Clerk):
            print("✓ Clerk client initialized successfully")
        else:
            print(f"✗ Clerk client is wrong type: {type(clerk_client)}")
            return False
        return True
    except Exception as e:
        print(f"✗ Clerk client test failed: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_models():
    """Test model functionality"""
    try:
        from accounts.models import UserProfile
        count = UserProfile.objects.count()
        print(f"✓ Models working (UserProfile count: {count})")
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Django Backend Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("System Check", test_system_check),
        ("Clerk Client", test_clerk_client),
        ("Database", test_database),
        ("Models", test_models),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is ready to run.")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please review above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
