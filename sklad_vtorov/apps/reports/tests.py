from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
class DashboardTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
    def test_dashboard_after_login(self):
        user = get_user_model().objects.create_user(username="tester", password="StrongPass123!")
        self.client.login(username="tester", password="StrongPass123!")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
