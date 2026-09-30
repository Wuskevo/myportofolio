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

from .models import Credential, Experience, Project

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


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
        

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
			"title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
		]
        
        labels = {
			"title": "Project Name",
            "description": "Project Description",
            "tech_stack": "Tech Usedd",
            "project_url": "Project URL",
            "project_image_url": "Project Image URL",
		}
        
        widgets = {
			"title": TextInput(
       			attrs={
       				"placeholder": "Portfolio Website",
					"maxlength": 255
            	}
          	),
			"description": Textarea(
				attrs={
                    "placeholder": "Tell us about your project",
                    "rows": 3,
                }
			),
			"tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),

		}
        
        def clean_title(self):
            title = strip_tags(self.cleaned_data["title"]).strip()
            if not title:
                raise ValidationError("Project name can't contain only HTML tags.")
            return title
        
        def clean_tech_stack(self):
            return strip_tags(self.cleaned_data["tech_stack"]).strip()
        
        def clean_description(self):
            return strip_tags(self.cleaned_data["description"]).strip()