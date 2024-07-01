# books/tests.py
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserTests(APITestCase):

    def test_register_user(self):
        """
        Ensure we can register a new user.
        """
        url = reverse("register")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_login_user(self):
        """
        Ensure we can log in a user and get a token.
        """
        # Register the user first
        self.client.post(
            reverse("register"),
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )

        url = reverse("login")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
