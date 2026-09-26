"""Tests for project pages, CRUD forms, and the project JSON endpoint."""

from django.test import TestCase
from django.urls import reverse

from main.models import Project


class ProjectTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio Website",
            description="A Django portfolio website.",
            tech_stack="Django, Python, HTML, CSS",
            project_url="https://example.com/portfolio",
        )

    def test_projects_page_displays_project_and_edit_link(self):
        """Verify that the projects page renders project details and its edit URL."""
        response = self.client.get(reverse("main:show_projects"))

        # The response and template checks confirm the expected page is rendered.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        # Check the project data and edit route rendered in the project card.
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(
            response,
            reverse("main:update_project", args=[self.project.id]),
        )

    def test_projects_json_endpoint_returns_projects(self):
        """Verify that the project JSON endpoint returns stored project data."""
        response = self.client.get(reverse("main:get_projects_json"))

        # Check both the JSON response type and its serialized project values.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)

    def test_projects_json_endpoint_filters_by_title(self):
        """Verify that title searches exclude projects that do not match."""
        Project.objects.create(
            title="Game Jam Entry",
            description="A small game jam project.",
            tech_stack="Godot, GDScript",
        )

        response = self.client.get(
            reverse("main:get_projects_json"),
            {"title": "game"},
        )

        # The matching title is present and the unrelated project is excluded.
        self.assertContains(response, "Game Jam Entry")
        self.assertNotContains(response, self.project.title)

    def test_create_project(self):
        """Verify that submitting the project form creates a database record."""
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "New Project",
                "description": "A new project description.",
                "tech_stack": "Python",
                "project_url": "",
                "project_image_url": "",
            },
        )

        # Check the post-creation redirect and that the new record was saved.
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="New Project").exists())

    def test_update_project_form_posts_to_update_route(self):
        """Verify that editing a project submits to its update URL, not create."""
        response = self.client.get(
            reverse("main:update_project", args=[self.project.id])
        )

        # The action check guards against edits accidentally creating duplicates.
        self.assertContains(
            response,
            f'action="{reverse("main:update_project", args=[self.project.id])}"',
        )

    def test_update_project_changes_existing_record_without_duplicating(self):
        """Verify that an edit updates one project rather than creating another."""
        response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            {
                "title": "Updated Portfolio",
                "description": "Updated project description.",
                "tech_stack": "Django, Python",
                "project_url": "",
                "project_image_url": "",
            },
        )

        # Confirm the response, persisted edits, and unchanged record count.
        self.assertRedirects(response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Portfolio")
        self.assertEqual(Project.objects.count(), 1)

    def test_delete_project(self):
        """Verify that posting the delete route removes the selected project."""
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id])
        )

        # Check that deletion returns to the project list and removes the record.
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())