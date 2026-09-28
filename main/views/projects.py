from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ProjectForm
from main.models import Project

from .common import NAME, filter_by_title, is_editor_user


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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
    projects = filter_by_title(Project.objects.all(), title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    projects = filter_by_title(Project.objects.all(), title_query)

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
    if not request.user.is_superuser:
        raise PermissionDenied

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