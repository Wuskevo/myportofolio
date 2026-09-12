import uuid

from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

"""
Added this instead of achievements and certifications because there is a lot of overlap currently
Instead of complicated inheritance, enums are used, following the pattern from [Experience]
"""
class Credential(models.Model):
    CREDENTIAL_CATEGORIES = [
        ("certification", "Certification"),
        ("award", "Award"),
        ("competition", "Competition"),
        ("scholarship", "Scholarship")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CREDENTIAL_CATEGORIES,
        default="certification",
    )

    ## organization or event
    issuer = models.CharField(max_length=255)

    ## date of earning this credential
    date_received = models.DateField()

    ## date of expiry, may not apply
    expiry_date = models.DateField(blank=True, null=True)

    ## link/url to some source to verify this credential
    credential_url = models.URLField(blank=True)

    ## image relevant to this credential like trophy, certificate, badge, etc
    image = models.ImageField(
        upload_to="credentials/",
        blank=True,
        null=True
    )
    

        