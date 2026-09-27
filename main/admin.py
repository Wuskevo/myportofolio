from django.contrib import admin
from .models import Experience, Credential, Project

# Register your models here.
admin.site.register(Experience)
admin.site.register(Credential)
admin.site.register(Project)

# TODO: Create the Editor group in Django Admin with only model change permissions.