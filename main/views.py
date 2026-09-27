import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.models import Experience, Credential, Project
from main.forms import CredentialForm, ExperienceForm, ProjectForm

NAME = "Clement Kevin Tanadi"
NPM = "2506632892"
STUDY_PROGRAM = "Undergrad Computer Science"
BIO = (
    	"CS student at Universitas Indonesia passionate in Game Development and Competitive Programming."
    	"Currently working on indie games joining jams and competitions."
    )

EDITOR_STR = "Editor"

def is_editor_user(user):
    return user.is_authenticated and user.groups.filter(name=EDITOR_STR).exists()

def register(request):
    form = UserCreationForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect("main:login")
    
    context = {
		"name": NAME,
		"form": form,
	}
    
    return render(request, "forms/register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
    
    context = {
		"name": NAME,
		"form": form,
	}
    
    return render(request, "forms/login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
    context = {
        "name": NAME,
        "npm": NPM,
        "study_program": STUDY_PROGRAM,
        "bio": BIO,
        "project_list": Project.objects.order_by("title"),
        "last_login": last_login,
        "is_editor": is_editor_user(request.user),
    }
    return render(request, "index.html", context)

#
# Experiences CRUD with json data delivery
#

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
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
        "is_editor": is_editor_user(request.user),
    }
    return render(request, "experiences.html", context)

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser and not is_editor_user(request.user):
        raise PermissionDenied

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

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience successfully removed!")
        return redirect("main:show_experiences")

    return redirect("main:show_experiences")

@login_required(login_url="/login/")
@require_POST
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.user in experience.starred_by.all():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    return redirect("main:show_experiences")

#
# Credentials CRUD with json data delivery
#

@login_required(login_url="/login/") 
def create_credential(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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
        "is_editor": is_editor_user(request.user),
    }
    return render(request, "credentials.html", context)

@login_required(login_url="/login/") 
def update_credential(request, credential_id):
    if not request.user.is_superuser and not is_editor_user(request.user):
        raise PermissionDenied
    
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

@login_required(login_url="/login/")  
def delete_credential(request, credential_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    credential = get_object_or_404(Credential, pk=credential_id)

    if request.method == "POST":
        credential.delete()
        messages.success(request, "Credential successfully removed!")

    return redirect("main:show_credentials")

#
# Projects CRUD with json data delivery
#

@login_required(login_url="/login/") 
def create_project(request):

    if not request.user.is_superuser: # checks if logged-in account is the superuser
        raise PermissionDenied # stops request with 403
	
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

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
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
        "is_editor": is_editor_user(request.user),
    }
    return render(request, "projects.html", context)

@login_required(login_url="/login/") 
def update_project(request, project_id):
    if not request.user.is_superuser and not is_editor_user(request.user):
        raise PermissionDenied
    
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

@login_required(login_url="/login/") 
def delete_project(request, project_id):
    
    if not request.user.is_superuser: # checks if logged-in account is the superuser
        raise PermissionDenied # stops request with 403

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "project successfully removed!")

    return redirect("main:show_projects")

@login_required(login_url="/login")
def toggle_project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
        
    return redirect("main:show_projects")
