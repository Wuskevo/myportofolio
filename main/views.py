from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Credential
from main.forms import CredentialForm, ExperienceForm

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


def show_experiences(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Clement Kevin Tanadi",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experiences.html", context)


def show_credentials(request):
    json_response = get_credentials_json(request)
    credentials = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    credentials_by_category = {}
    for deserialized_credential in credentials:
        credential = deserialized_credential.object
        credentials_by_category.setdefault(credential.category, []).append(credential)

    context = {
        "name": "Clement Kevin Tanadi",
        "credentials_by_category": credentials_by_category,
    }
    return render(request, "credentials.html", context)

def create_experiences(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experiences")

    context = {
        "name": "Clement Kevin Tanadi",
        "form": form,
    }
    return render(request, "experiences_form.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def delete_experiences(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience successfully removed!")
        return redirect("main:show_experiences")

    return redirect("main:show_experiences")


def create_credentials(request):
    form = CredentialForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New credential successfully added!")
        return redirect("main:show_credentials")

    context = {
        "name": "Clement Kevin Tanadi",
        "form": form,
        "form_title": "Add New Credential",
        "submit_label": "Add Credential",
    }
    return render(request, "credentials_form.html", context)


def update_credentials(request, credential_id):
    credential = get_object_or_404(Credential, pk=credential_id)
    form = CredentialForm(
        request.POST or None,
        request.FILES or None,
        instance=credential,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Credential successfully updated!")
        return redirect("main:show_credentials")

    context = {
        "name": "Clement Kevin Tanadi",
        "form": form,
        "form_title": "Update Credential",
        "submit_label": "Update Credential",
    }
    return render(request, "credentials_form.html", context)


def delete_credentials(request, credential_id):
    credential = get_object_or_404(Credential, pk=credential_id)

    if request.method == "POST":
        credential.delete()
        messages.success(request, "Credential successfully removed!")

    return redirect("main:show_credentials")


def get_credentials_json(request):
    title_query = request.GET.get("title", "").strip()
    credentials = Credential.objects.all()

    if title_query:
        credentials = credentials.filter(title__icontains=title_query)

    credentials_json = serializers.serialize("json", credentials)
    return HttpResponse(credentials_json, content_type="application/json")