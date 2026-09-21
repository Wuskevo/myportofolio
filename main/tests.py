from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.forms import CredentialForm
from main.models import Experience, Credential


class MainTest(TestCase):
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

    def test_update_experiences(self):
        """Verify that posting the experience form updates the stored experience."""
        response = self.client.post(
            reverse("main:update_experiences", args=[self.experience.id]),
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
            reverse("main:update_experiences", args=[self.experience.id])
        )

        # See the content assertion above: assertContains checks rendered markup.
        self.assertContains(
            response,
            f'action="{reverse("main:update_experiences", args=[self.experience.id])}"',
        )

    def test_experience_page_has_update_link(self):
        """Verify that each experience card exposes its edit link."""
        response = self.client.get(reverse("main:show_experiences"))

        # See the content assertion above: assertContains checks rendered markup.
        self.assertContains(
            response,
            reverse("main:update_experiences", args=[self.experience.id]),
        )

class CredentialsTest(TestCase):
    def setUp(self):
        self.credentials = {}
        for category, _ in Credential.CREDENTIAL_CATEGORIES: 
            self.credentials[category] = Credential.objects.create(
                title=f"{category} title",
                issuer=f"{category} issuer",
                description=f"{category} description",
                category=category,
                date_received=timezone.now()
            )

    def test_credentials_page_accessible_and_correct_template(self):
        """Verify that the credentials page loads with the expected template."""
        response = self.client.get(reverse("main:show_credentials"))
        # See the status-code assertion above: assertEqual compares expected values.
        self.assertEqual(response.status_code, 200)
        # See the template assertion above: assertTemplateUsed verifies the rendered template.
        self.assertTemplateUsed(response, "credentials.html")

    def test_credentials_appear_grouped_by_category(self):
        """Verify that credentials appear under the correct category headings."""
        category_headings = {
            "certification": "My Certifications",
            "competition": "My Competitions",
            "award": "My Awards",
            "scholarship": "My Scholarships",
        }

        response = self.client.get(reverse("main:show_credentials"))
        for category, credential in self.credentials.items():
            # See the content assertion above: assertContains checks rendered content.
            self.assertContains(response, credential.title)
            # See the assertion above: assertContains checks rendered content.
            self.assertContains(response, credential.issuer)
            # See the assertion above: assertContains checks rendered content.
            self.assertContains(response, category_headings[category])

        # See the content assertion above: assertContains also supports occurrence counts.
        self.assertContains(response, 'title="Remove credential"', count=4)
        # See the assertion above: assertContains verifies repeated rendered content.
        self.assertContains(response, "Edit Credential", count=4)

    def test_empty_category_shows_placeholder(self):
        """Verify that an empty credential category shows its placeholder."""
        self.credentials["certification"].delete()
        response = self.client.get(reverse("main:show_credentials"))

        # See the content assertion above: assertContains verifies the placeholder count.
        self.assertContains(response, "No credentials have been added yet.", count=1)
        # The other three categories still have their credential rendered
        self.assertContains(response, self.credentials["competition"].title)
        self.assertContains(response, self.credentials["award"].title)
        self.assertContains(response, self.credentials["scholarship"].title)

    def test_all_categories_empty(self):
        """Verify that every empty credential category shows a placeholder."""
        Credential.objects.all().delete()
        response = self.client.get(reverse("main:show_credentials"))

        # See the content assertion above: assertContains verifies the total count.
        self.assertContains(response, "No credentials have been added yet.", count=4)

    def test_credential_expiry_states(self):
        """Verify the displayed expiry text for expiring and non-expiring credentials."""
        self.credentials["competition"].delete()
        self.credentials["award"].delete()
        self.credentials["scholarship"].delete()
        cred = self.credentials["certification"]

        response = self.client.get(reverse("main:show_credentials"))
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, "Never expires")

        cred.expiry_date = timezone.now()
        cred.save()
        response = self.client.get(reverse("main:show_credentials"))
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, "Expires")
        # See the earlier negative-content assertion: assertNotContains checks excluded content.
        self.assertNotContains(response, "Never expires")

    def test_credential_url_states(self):
        """Verify the displayed verification link and fallback text."""
        self.credentials["competition"].delete()
        self.credentials["award"].delete()
        self.credentials["scholarship"].delete()
        cred = self.credentials["certification"]

        response = self.client.get(reverse("main:show_credentials"))
        # See the content assertion above: assertContains checks rendered content.
        self.assertContains(response, "Verification not provided")

        cred.credential_url = "https://example.com/verify"
        cred.save()
        response = self.client.get(reverse("main:show_credentials"))
        # See the content assertion above: assertContains checks rendered markup.
        self.assertContains(response, f'href="{cred.credential_url}"')
        # See the earlier negative-content assertion: assertNotContains checks excluded content.
        self.assertNotContains(response, "Verification not provided")

    def test_credential_form_has_expected_fields(self):
        """Verify that the credential form exposes the expected model fields."""
        form = CredentialForm()

        # See the assertion above: assertEqual compares expected collections or values.
        self.assertEqual(
            list(form.fields),
            [
                "title",
                "description",
                "category",
                "issuer",
                "date_received",
                "expiry_date",
                "credential_url",
                "image",
            ],
        )
        # assertNotIn checks that an unwanted value is absent from a collection.
        self.assertNotIn("id", form.fields)

    def test_credential_form_validates_required_and_optional_fields(self):
        """Verify required fields and optional credential fields validate correctly."""
        form = CredentialForm(
            data={
                "title": "Django Developer Certificate",
                "description": "A certificate for Django development.",
                "category": "certification",
                "issuer": "Django Software Foundation",
                "date_received": "2026-09-18",
                "expiry_date": "",
                "credential_url": "https://example.com/verify",
            }
        )

        # See the model assertion above: assertTrue verifies a condition is true.
        self.assertTrue(form.is_valid())
        # See the assertion above: assertEqual verifies cleaned form values.
        self.assertEqual(form.cleaned_data["date_received"].year, 2026)
        # See the assertion above: assertEqual verifies cleaned form values.
        self.assertIsNone(form.cleaned_data["expiry_date"])
        # See the assertion above: assertEqual verifies cleaned form values.
        self.assertEqual(
            form.cleaned_data["credential_url"],
            "https://example.com/verify",
        )

    def test_credentials_json_endpoint_returns_credentials(self):
        """Verify that the credential endpoint returns JSON with stored data."""
        response = self.client.get(reverse("main:get_credentials_json"))

        # See the status-code assertion above: assertEqual compares expected values.
        self.assertEqual(response.status_code, 200)
        # See the assertion above: assertEqual verifies the response content type.
        self.assertEqual(response["Content-Type"], "application/json")
        # See the content assertion above: assertContains checks returned JSON content.
        self.assertContains(response, self.credentials["certification"].title)

    def test_credentials_json_endpoint_filters_by_title(self):
        """Verify that the credential JSON endpoint filters by title."""
        response = self.client.get(
            reverse("main:get_credentials_json"),
            {"title": "award"},
        )

        # See the content assertion above: assertContains checks filtered JSON content.
        self.assertContains(response, self.credentials["award"].title)
        # See the earlier negative-content assertion: assertNotContains checks excluded data.
        self.assertNotContains(response, self.credentials["certification"].title)

    def test_create_credentials(self):
        """Verify that posting the credential form creates a credential."""
        response = self.client.post(
            reverse("main:create_credentials"),
            {
                "title": "New Credential",
                "description": "A new credential.",
                "category": "certification",
                "issuer": "Test Issuer",
                "date_received": "2026-09-18",
                "expiry_date": "",
                "credential_url": "https://example.com/new",
            },
        )

        # See the redirect assertion above: assertRedirects verifies the destination URL.
        self.assertRedirects(response, reverse("main:show_credentials"))
        # assertTrue checks that the query returns at least one matching object.
        self.assertTrue(Credential.objects.filter(title="New Credential").exists())

    def test_update_credentials(self):
        """Verify that posting the credential form updates a credential."""
        credential = self.credentials["certification"]
        response = self.client.post(
            reverse("main:update_credentials", args=[credential.id]),
            {
                "title": "Updated Credential",
                "description": credential.description,
                "category": credential.category,
                "issuer": credential.issuer,
                "date_received": "2026-09-18",
                "expiry_date": "",
                "credential_url": "",
            },
        )

        # See the redirect assertion above: assertRedirects verifies the destination URL.
        self.assertRedirects(response, reverse("main:show_credentials"))
        credential.refresh_from_db()
        # See the assertion above: assertEqual verifies the saved model value.
        self.assertEqual(credential.title, "Updated Credential")

    def test_delete_credentials(self):
        """Verify that posting the delete form removes a credential."""
        credential = self.credentials["certification"]
        response = self.client.post(
            reverse("main:delete_credentials", args=[credential.id])
        )

        # See the redirect assertion above: assertRedirects verifies the destination URL.
        self.assertRedirects(response, reverse("main:show_credentials"))
        # See the earlier assertTrue example: assertFalse verifies the object no longer exists.
        self.assertFalse(Credential.objects.filter(pk=credential.id).exists())