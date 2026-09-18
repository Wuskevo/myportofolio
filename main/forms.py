from django.forms import (
    DateInput,
    DateTimeInput,
    FileInput,
    ModelForm,
    Select,
    Textarea,
    TextInput,
    URLInput,
)

from .models import Credential, Experience


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Experience Title",
            "description": "Experience Description",
            "category": "Experience Category",
            "thumbnail": "Thumbnail URL",
            "ended_at": "End Date",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell us about your experience in this project",
                    "rows": 4,
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/thumbnail.jpg",
                }
            ),
            "ended_at": DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "type": "datetime-local",
                    "placeholder": "YYYY-MM-DDTHH:MM",
                },
            ),
        }


class CredentialForm(ModelForm):
    class Meta:
        model = Credential
        fields = [
            "title",
            "description",
            "category",
            "issuer",
            "date_received",
            "expiry_date",
            "credential_url",
            "image",
        ]

        labels = {
            "title": "Credential Title",
            "description": "Credential Description",
            "category": "Credential Category",
            "issuer": "Issuing Organization or Event",
            "date_received": "Date Received",
            "expiry_date": "Expiry Date",
            "credential_url": "Verification URL",
            "image": "Credential Image",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "AWS Certified Developer",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe this credential",
                    "rows": 4,
                }
            ),
            "category": Select(),
            "issuer": TextInput(
                attrs={
                    "placeholder": "Issuing organization or event",
                    "maxlength": 255,
                }
            ),
            "date_received": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                },
            ),
            "expiry_date": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                },
            ),
            "credential_url": URLInput(
                attrs={
                    "placeholder": "https://example.com/verify",
                }
            ),
            "image": FileInput(),
        }