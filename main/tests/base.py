from django.contrib.auth.models import User
from django.test import TestCase


class BasePortfolioTestCase(TestCase):
    def login_as_owner(self):
        owner = User.objects.create_superuser(
            username="test-owner",
            email="owner@example.com",
            password="password",
        )
        self.client.force_login(owner)