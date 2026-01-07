from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class SignupTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_successful_signup(self):
        data = {
            "name": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        response = self.client.post("/api/accounts/signup/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_signup_with_long_name(self):
        long_name = "a" * 151
        data = {
            "name": long_name,
            "email": "longname@example.com",
            "password": "testpassword"
        }
        response = self.client.post("/api/accounts/signup/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_signup_with_existing_email(self):
        User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        data = {
            "name": "anotheruser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        response = self.client.post("/api/accounts/signup/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        
    def test_signup_with_existing_name(self):
        User.objects.create_user(username="testuser", email="test1@example.com", password="testpassword")
        data = {
            "name": "testuser",
            "email": "test2@example.com",
            "password": "testpassword"
        }
        response = self.client.post("/api/accounts/signup/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
