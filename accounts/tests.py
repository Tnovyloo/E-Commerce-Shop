import pytest
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Account

class TestAccountsApp(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_user_success(self):
        """Testing creating a user is successful"""

        payload = {
            "first_name": "testname",
            "last_name": "testlastname",
            "phone_number": "123123123",
            "email": "example@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }

        url = reverse('register')

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 302)

    def test_login_user_success(self):
        """Testing login a user is successful"""
        payload = {
            "email": "example@example.com",
            "password": "password123",
        }

        user = Account.objects.create(**payload)

        url = reverse('login')
        response = self.client.post(url, payload, follow=True)

        # User needs to activate account.
        self.assertFalse(response.context['user'].is_active)

    def test_forgot_password_page(self):
        """Testing if forgot page is active"""
        payload = {
            "email": "example@example.com",
            "password": "password123",
        }

        user = Account.objects.create(**payload)
        user.is_active = True
        user.save()

        self.client.login(**payload)

        url = reverse("forgotPassword")
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

    def test_logout(self):
        """Testing if logout page is active"""
        payload = {
            "email": "example@example.com",
            "password": "password123",
        }

        user = Account.objects.create(**payload)
        user.is_active = True
        user.save()

        self.client.login(**payload)

        url = reverse("dashboard")
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)

        response = self.client.logout()
        self.assertEqual(200, response.status_code)

    def test_dashboard_page(self):
        """Testing if dashboard page is active"""
        payload = {
            "email": "example@example.com",
            "password": "password123",
        }

        user = Account.objects.create(**payload)
        user.is_active = True
        user.save()

        self.client.login(**payload)

        url = reverse("dashboard")
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)

