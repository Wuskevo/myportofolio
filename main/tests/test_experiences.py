"""Tests for experience model behavior, pages, forms, and JSON endpoints."""

from datetime import timedelta

from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse
from django.utils import timezone

from main.forms import ExperienceForm
from main.models import Experience
from main.tests.base import BasePortfolioTestCase


class ExperienceTests(BasePortfolioTestCase):
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
        """Verify that the experience page renders the AJAX shell and page metadata."""
        response = self.client.get(reverse("main:show_experiences"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, 'id="experience-sort"')
        self.assertContains(response, 'class="experience-timeline hide"')
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="experience"')

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

    def test_experiences_json_endpoint_sorts_by_start_date(self):
        now = timezone.now()
        middle_experience = Experience.objects.create(
            title="Middle Experience",
            description="Middle experience description.",
            category="research",
        )
        newest_experience = Experience.objects.create(
            title="Newest Experience",
            description="Newest experience description.",
            category="research",
        )
        Experience.objects.filter(pk=self.experience.pk).update(
            started_at=now - timedelta(days=90)
        )
        Experience.objects.filter(pk=middle_experience.pk).update(
            started_at=now - timedelta(days=60)
        )
        Experience.objects.filter(pk=newest_experience.pk).update(
            started_at=now - timedelta(days=30)
        )

        for sort_order, expected_ids in (
            (
                "start-desc",
                [newest_experience.pk, middle_experience.pk, self.experience.pk],
            ),
            (
                "start-asc",
                [self.experience.pk, middle_experience.pk, newest_experience.pk],
            ),
        ):
            with self.subTest(sort=sort_order):
                response = self.client.get(
                    reverse("main:get_experiences_json"),
                    {"sort": sort_order},
                )
                self.assertEqual(
                    [entry["pk"] for entry in response.json()],
                    [str(experience_id) for experience_id in expected_ids],
                )

    def test_experiences_json_endpoint_combines_title_filter_and_sort(self):
        now = timezone.now()
        older_match = Experience.objects.create(
            title="Matching Older Role",
            description="Older matching role description.",
            category="research",
        )
        newer_match = Experience.objects.create(
            title="Matching Newer Role",
            description="Newer matching role description.",
            category="research",
        )
        Experience.objects.filter(pk=older_match.pk).update(
            started_at=now - timedelta(days=60)
        )
        Experience.objects.filter(pk=newer_match.pk).update(
            started_at=now - timedelta(days=30)
        )

        response = self.client.get(
            reverse("main:get_experiences_json"),
            {"title": "matching", "sort": "start-asc"},
        )

        self.assertEqual(
            [entry["pk"] for entry in response.json()],
            [str(older_match.pk), str(newer_match.pk)],
        )

    def test_experiences_json_endpoint_sorts_end_dates_with_ongoing_first(self):
        now = timezone.now()
        older_completed = Experience.objects.create(
            title="Older Completed Experience",
            description="Older completed experience description.",
            category="research",
            ended_at=now - timedelta(days=30),
        )
        newer_completed = Experience.objects.create(
            title="Newer Completed Experience",
            description="Newer completed experience description.",
            category="research",
            ended_at=now - timedelta(days=1),
        )

        for sort_order, expected_ids in (
            (
                "end-desc",
                [self.experience.pk, newer_completed.pk, older_completed.pk],
            ),
            (
                "end-asc",
                [self.experience.pk, older_completed.pk, newer_completed.pk],
            ),
        ):
            with self.subTest(sort=sort_order):
                response = self.client.get(
                    reverse("main:get_experiences_json"),
                    {"sort": sort_order},
                )
                self.assertEqual(
                    [entry["pk"] for entry in response.json()],
                    [str(experience_id) for experience_id in expected_ids],
                )

    def test_experience_page_preserves_selected_sort_option(self):
        response = self.client.get(
            reverse("main:show_experiences"),
            {"sort": "end-asc"},
        )

        self.assertEqual(response.context["sort_query"], "end-asc")
        self.assertRegex(
            response.content.decode(),
            r'<option value="end-asc"\s+selected>End: oldest</option>',
        )

    def test_experience_page_displays_database_data(self):
        """Verify that the experience page configures the client-side JSON fetch."""
        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'id="search-input"')
        self.assertContains(
            response, 'const BASE_EXPERIENCE_ENDPOINT = "/experiences/json/";'
        )

    def test_experience_page_filters_by_title(self):
        """Verify that the search form keeps the current title filter in the page shell."""
        Experience.objects.create(
            title="Competitive Programming Coach",
            description="Mentored students in algorithmic problem solving.",
            category="volunteer",
        )

        response = self.client.get(
            reverse("main:show_experiences"),
            {"title": "coach"},
        )

        self.assertContains(response, 'value="coach"')
        self.assertContains(response, 'name="title"')
        self.assertNotContains(response, 'value="PBP Teaching Assistant"')

    def test_empty_experience_page(self):
        """Verify that the experience page shows its empty-state shell."""
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(response, "No experiences have been added or found yet.")

    def test_completed_experience(self):
        """Verify that completed experiences are marked as finished in the model and JSON payload."""
        self.experience.ended_at = timezone.now()
        self.experience.save()

        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertFalse(self.experience.is_ongoing)
        item = next(
            entry for entry in response.json() if entry["pk"] == str(self.experience.id)
        )
        self.assertIsNotNone(item["fields"]["ended_at"])
        self.assertEqual(item["fields"]["category"], "part-time")

    def test_update_experience(self):
        """Verify that posting the experience form updates the stored experience."""
        self.login_as_owner()
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
        self.login_as_owner()
        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )

        # See the content assertion above: assertContains checks rendered markup.
        self.assertContains(
            response,
            f'action="{reverse("main:update_experience", args=[self.experience.id])}"',
        )

    def test_anonymous_user_does_not_see_experience_actions(self):
        """Visitors can read the page shell but do not see owner-only controls."""
        response = self.client.get(reverse("main:show_experiences"))

        self.assertNotContains(response, 'id="add-experience-modal"')
        self.assertNotContains(
            response,
            reverse("main:update_experience", args=[self.experience.id]),
        )
        self.assertNotContains(
            response,
            reverse("main:delete_experience", args=[self.experience.id]),
        )
        self.assertNotContains(
            response,
            reverse("main:toggle_experience_star", args=[self.experience.id]),
        )
        self.assertContains(response, 'id="experience-search-form"')

    def test_editor_sees_experience_edit_but_not_create_or_delete(self):
        editor = User.objects.create_user(username="editor", password="password")
        permission = Permission.objects.get(
            content_type__app_label="main",
            codename="change_experience",
        )
        editor_group = Group.objects.create(name="Editor")
        editor_group.permissions.add(permission)
        editor.groups.add(editor_group)
        self.client.force_login(editor)

        response = self.client.get(reverse("main:show_experiences"))

        self.assertTrue(response.context["is_editor"])
        self.assertFalse(response.context["user"].is_superuser)
        self.assertContains(response, 'const IS_EDITOR = "true" === "true";')
        self.assertContains(response, 'const IS_SUPERUSER = "false" === "true";')
        self.assertNotContains(response, 'id="add-experience-modal"')

    def test_superuser_sees_all_experience_actions(self):
        owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password="password",
        )
        self.client.force_login(owner)

        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(response, 'id="add-experience-modal"')
        self.assertContains(response, reverse("main:create_experience_ajax"))
        self.assertContains(
            response,
            reverse(
                "main:update_experience",
                args=["00000000-0000-0000-0000-000000000000"],
            ),
        )
        self.assertContains(
            response,
            reverse(
                "main:delete_experience",
                args=["00000000-0000-0000-0000-000000000000"],
            ),
        )

    def test_delete_experience(self):
        """Verify that posting the delete form removes an experience."""
        self.login_as_owner()
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

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_create_experience_ajax_returns_created_experience(self):
        self.login_as_owner()
        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": "AJAX Experience",
                "description": "Created from the experience modal.",
                "category": "research",
                "thumbnail": "https://example.com/experience.jpg",
                "ended_at": "",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertTrue(Experience.objects.filter(title="AJAX Experience").exists())
        self.assertEqual(response.json()["message"], "Experience added successfully.")
