from django.forms import DateTimeInput, ModelForm, Select, Textarea, TextInput, URLInput

from .models import Experience


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