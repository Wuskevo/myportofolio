from django.test import TestCase
from django.urls import reverse

from main.models import Experience


class MainTests(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        """Verify the home page loads and links back to the main sections."""
        response = self.client.get(reverse("main:show_main"))

        # assertEqual checks that the response uses the expected HTTP status.
        self.assertEqual(response.status_code, 200)
        # assertTemplateUsed checks that Django rendered the expected template.
        self.assertTemplateUsed(response, "index.html")
        # assertNotContains checks that unrelated experience data is absent.
        self.assertNotContains(response, self.experience.title)
        # See the assertion above: assertContains checks that expected page content exists.
        self.assertContains(response, f'href="{reverse("main:show_experiences")}"')

    def test_nonexistent_page_returns_404(self):
        """Verify that an unknown URL returns a not-found response."""
        response = self.client.get("/a-page-that-does-not-exist/")

        # See the status-code assertion above: assertEqual compares expected values.
        self.assertEqual(response.status_code, 404)