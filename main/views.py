from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Credential, Project
from main.forms import CredentialForm, ExperienceForm, ProjectForm

NAME = "Clement Kevin Tanadi"
NPM = "2506632892"
STUDY_PROGRAM = "Undergrad Computer Science"
BIO = (
    	"CS student at Universitas Indonesia passionate in Game Development and Competitive Programming."
    	"Currently working on indie games joining jams and competitions."
    )

def show_main(request):
    context = {
        "name": NAME,
        "npm": NPM,
        "study_program": STUDY_PROGRAM,
        "bio": BIO,
    }
    return render(request, "index.html", context)

#
# Experiences CRUD with json data delivery
#

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experiences")

    context = {
        "name": NAME,
        "form": form,
    }
    return render(request, "forms/experiences_form.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def show_experiences(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": NAME,
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experiences.html", context)

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience successfully updated!")
        return redirect("main:show_experiences")

    context = {
        "name": NAME,
        "form": form,
        "form_title": "Update Experience",
        "submit_label": "Update Experience",
        "experience_id": experience.id,
    }
    return render(request, "forms/experiences_form.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience successfully removed!")
        return redirect("main:show_experiences")

    return redirect("main:show_experiences")

#
# Credentials CRUD with json data delivery
#

def create_credential(request):
    form = CredentialForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New credential successfully added!")
        return redirect("main:show_credentials")

    context = {
        "name": NAME,
        "form": form,
        "form_title": "Add New Credential",
        "submit_label": "Add Credential",
    }
    return render(request, "forms/credentials_form.html", context)

def get_credentials_json(request):
    title_query = request.GET.get("title", "").strip()
    credentials = Credential.objects.all()

    if title_query:
        credentials = credentials.filter(title__icontains=title_query)

    credentials_json = serializers.serialize("json", credentials)
    return HttpResponse(credentials_json, content_type="application/json")

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
        "name": NAME,
        "credentials_by_category": credentials_by_category,
    }
    return render(request, "credentials.html", context)

def update_credential(request, credential_id):
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
        "name": NAME,
        "form": form,
        "form_title": "Update Credential",
        "submit_label": "Update Credential",
    }
    return render(request, "forms/credentials_form.html", context)

def delete_credential(request, credential_id):
    credential = get_object_or_404(Credential, pk=credential_id)

    if request.method == "POST":
        credential.delete()
        messages.success(request, "Credential successfully removed!")

    return redirect("main:show_credentials")

#
# Projects CRUD with json data delivery
#

def create_project(request):
    form = ProjectForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New project successfully added!")
        return redirect("main:show_projects")
    
    context = {
		"name": NAME,
		"form": form,
	}
    
    return render(request, "forms/projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": NAME,
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(
        request.POST or None,
        request.FILES or None,
        instance=project,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project successfully updated!")
        return redirect("main:show_projects")

    context = {
        "name": NAME,
        "form": form,
        "form_title": "Update Project",
        "submit_label": "Update Project",
        "project_id": project.id,
    }
    return render(request, "forms/projects_form.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "project successfully removed!")

    return redirect("main:show_projects")