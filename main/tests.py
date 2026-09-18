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
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

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
        response = self.client.get(reverse("main:show_credentials"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "credentials.html")

    def test_credentials_appear_grouped_by_category(self):
        category_headings = {
            "certification": "My Certifications",
            "competition": "My Competitions",
            "award": "My Awards",
            "scholarship": "My Scholarships",
        }

        response = self.client.get(reverse("main:show_credentials"))
        for category, credential in self.credentials.items():
            self.assertContains(response, credential.title)
            self.assertContains(response, credential.issuer)
            self.assertContains(response, category_headings[category])

        self.assertContains(response, 'title="Remove credential"', count=4)
        self.assertContains(response, "Edit Credential", count=4)

    def test_empty_category_shows_placeholder(self):
        self.credentials["certification"].delete()
        response = self.client.get(reverse("main:show_credentials"))

        self.assertContains(response, "No credentials have been added yet.", count=1)
        # The other three categories still have their credential rendered
        self.assertContains(response, self.credentials["competition"].title)
        self.assertContains(response, self.credentials["award"].title)
        self.assertContains(response, self.credentials["scholarship"].title)

    def test_all_categories_empty(self):
        Credential.objects.all().delete()
        response = self.client.get(reverse("main:show_credentials"))

        self.assertContains(response, "No credentials have been added yet.", count=4)

    def test_credential_expiry_states(self):
        self.credentials["competition"].delete()
        self.credentials["award"].delete()
        self.credentials["scholarship"].delete()
        cred = self.credentials["certification"]

        response = self.client.get(reverse("main:show_credentials"))
        self.assertContains(response, "Never expires")

        cred.expiry_date = timezone.now()
        cred.save()
        response = self.client.get(reverse("main:show_credentials"))
        self.assertContains(response, "Expires")
        self.assertNotContains(response, "Never expires")

    def test_credential_url_states(self):
        self.credentials["competition"].delete()
        self.credentials["award"].delete()
        self.credentials["scholarship"].delete()
        cred = self.credentials["certification"]

        response = self.client.get(reverse("main:show_credentials"))
        self.assertContains(response, "Verification not provided")

        cred.credential_url = "https://example.com/verify"
        cred.save()
        response = self.client.get(reverse("main:show_credentials"))
        self.assertContains(response, f'href="{cred.credential_url}"')
        self.assertNotContains(response, "Verification not provided")

    def test_credential_form_has_expected_fields(self):
        form = CredentialForm()

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
        self.assertNotIn("id", form.fields)

    def test_credential_form_validates_required_and_optional_fields(self):
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

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["date_received"].year, 2026)
        self.assertIsNone(form.cleaned_data["expiry_date"])
        self.assertEqual(
            form.cleaned_data["credential_url"],
            "https://example.com/verify",
        )

    def test_credentials_json_endpoint_returns_credentials(self):
        response = self.client.get(reverse("main:get_credentials_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertContains(response, self.credentials["certification"].title)

    def test_credentials_json_endpoint_filters_by_title(self):
        response = self.client.get(
            reverse("main:get_credentials_json"),
            {"title": "award"},
        )

        self.assertContains(response, self.credentials["award"].title)
        self.assertNotContains(response, self.credentials["certification"].title)

    def test_create_credentials(self):
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

        self.assertRedirects(response, reverse("main:show_credentials"))
        self.assertTrue(Credential.objects.filter(title="New Credential").exists())

    def test_update_credentials(self):
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

        self.assertRedirects(response, reverse("main:show_credentials"))
        credential.refresh_from_db()
        self.assertEqual(credential.title, "Updated Credential")

    def test_delete_credentials(self):
        credential = self.credentials["certification"]
        response = self.client.post(
            reverse("main:delete_credentials", args=[credential.id])
        )

        self.assertRedirects(response, reverse("main:show_credentials"))
        self.assertFalse(Credential.objects.filter(pk=credential.id).exists())