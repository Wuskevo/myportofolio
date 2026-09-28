from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import ExperienceForm
from main.models import Experience

from .common import NAME, filter_by_title, is_editor_user


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
    experiences = filter_by_title(Experience.objects.all(), title_query)

    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(experiences_json, content_type="application/json")


def show_experiences(request):
    title_query = request.GET.get("title", "").strip()
    experiences = filter_by_title(Experience.objects.all(), title_query)

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