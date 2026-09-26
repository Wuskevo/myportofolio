"""Tests for experience model behavior, pages, forms, and JSON endpoints."""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.forms import ExperienceForm
from main.models import Experience


class ExperienceTests(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_experience_model(self):
        """Verify the experience string representation and ongoing state."""
        # See the content assertion above: assertEqual compares expected values.
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        # See the assertion above: assertEqual verifies an exact model value.
        self.assertEqual(self.experience.category, "part-time")
        # assertTrue checks that a value evaluates to True.
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        """Verify that an experience appears on the rendered experience page."""
        response = self.client.get(reverse("main:show_experiences"))

        # See the status-code assertion above: assertEqual compares expected values.
        self.assertEqual(response.status_code, 200)
        # See the template assertion above: assertTemplateUsed verifies the rendered template.
        self.assertTemplateUsed(response, "experiences.html")
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, self.experience.title)
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, self.experience.description)
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, "Part-Time")
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, "Ongoing")
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_experiences_json_endpoint_returns_experiences(self):
        """Verify that the experience endpoint returns JSON with stored data."""
        response = self.client.get(reverse("main:get_experiences_json"))

        # See the status-code assertion above: assertEqual compares expected values.
        self.assertEqual(response.status_code, 200)
        # See the assertion above: assertEqual also verifies the response content type.
        self.assertEqual(response["Content-Type"], "application/json")
        # See the content assertion above: assertContains checks returned JSON content.
        self.assertContains(response, self.experience.title)
        # See the content assertion above: assertContains checks returned JSON content.
        self.assertContains(response, self.experience.description)

    def test_experiences_json_endpoint_filters_by_title(self):
        """Verify that the experience JSON endpoint filters by title."""
        Experience.objects.create(
            title="Competitive Programming Coach",
            description="Mentored students in algorithmic problem solving.",
            category="volunteer",
        )

        response = self.client.get(
            reverse("main:get_experiences_json"),
            {"title": "coach"},
        )

        # See the content assertion above: assertContains checks filtered JSON content.
        self.assertContains(response, "Competitive Programming Coach")
        # See the earlier negative-content assertion: assertNotContains checks excluded data.
        self.assertNotContains(response, self.experience.title)

    def test_experience_page_displays_deserialized_json_data(self):
        """Verify that deserialized JSON data is displayed by the experience page."""
        response = self.client.get(reverse("main:show_experiences"))

        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, self.experience.title)
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, self.experience.get_category_display())

    def test_empty_experience_page(self):
        """Verify that the experience page shows its empty-state message."""
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experiences"))

        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        """Verify that completed experiences show Completed instead of Ongoing."""
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experiences"))

        # assertFalse checks that a value evaluates to False.
        self.assertFalse(self.experience.is_ongoing)
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, "Completed")
        # See the earlier negative-content assertion: assertNotContains checks excluded content.
        self.assertNotContains(response, "Ongoing")

    def test_update_experience(self):
        """Verify that posting the experience form updates the stored experience."""
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Updated Teaching Assistant",
                "description": "Updated experience description.",
                "category": "research",
                "thumbnail": "https://example.com/updated.jpg",
                "ended_at": "",
            },
        )

        # assertRedirects checks both the redirect response and its destination URL.
        self.assertRedirects(response, reverse("main:show_experiences"))
        self.experience.refresh_from_db()
        # See the assertion above: assertEqual compares expected values.
        self.assertEqual(self.experience.title, "Updated Teaching Assistant")
        # See the assertion above: assertEqual verifies the saved model value.
        self.assertEqual(self.experience.category, "research")

    def test_update_experience_form_posts_to_update_view(self):
        """Verify that the edit form posts to the experience update URL."""
        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )

        # See the content assertion above: assertContains checks rendered markup.
        self.assertContains(
            response,
            f'action="{reverse("main:update_experience", args=[self.experience.id])}"',
        )

    def test_experience_page_has_update_link(self):
        """Verify that each experience card exposes its edit link."""
        response = self.client.get(reverse("main:show_experiences"))

        # See the content assertion above: assertContains checks rendered markup.
        self.assertContains(
            response,
            reverse("main:update_experience", args=[self.experience.id]),
        )

    def test_delete_experience(self):
        """Verify that posting the delete form removes an experience."""
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        # See the redirect assertion above: assertRedirects verifies the destination URL.
        self.assertRedirects(response, reverse("main:show_experiences"))
        # See the earlier assertFalse example: assertFalse verifies the object no longer exists.
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_experience_form_rejects_missing_required_fields(self):
        """Verify that the experience form rejects a submission without required data."""
        form = ExperienceForm(data={})

        # See the earlier assertTrue example: assertFalse verifies invalid form state.
        self.assertFalse(form.is_valid())
        # assertIn checks that a required field appears in the form errors.
        self.assertIn("title", form.errors)
