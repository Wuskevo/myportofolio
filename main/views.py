from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Credential
from main.forms import ExperienceForm

def show_main(request):
    context = {
        "name": "Clement Kevin Tanadi",
        "npm": "2506632892",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia passionate in Game Development and Competitive Programming."
            "Currently working on indie games joining jams and competitions."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Clement Kevin Tanadi",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_credential(request):
    context = {
        "name": "Clement Kevin Tanadi",
        "credentials_by_category": Credential.grouped_by_category(),
    }
    return render(request, "credential.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experience")

    context = {
        "name": "Clement Kevin Tanadi",
        "form": form,
    }
    return render(request, "experience_form.html", context)