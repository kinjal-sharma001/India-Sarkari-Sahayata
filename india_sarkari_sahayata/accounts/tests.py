from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_candidate_registration_logs_user_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "candidate1",
                "email": "candidate1@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="candidate1").exists())

    def test_login_and_logout_flow(self):
        user = User.objects.create_user(username="candidate2", password="StrongPass123!", email="c2@example.com")
        login_response = self.client.post(
            reverse("login"),
            {"username": user.username, "password": "StrongPass123!"},
        )
        self.assertRedirects(login_response, reverse("home"))

        logout_response = self.client.post(reverse("logout"))
        self.assertRedirects(logout_response, reverse("login"))
