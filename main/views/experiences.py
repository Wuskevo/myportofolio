from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
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
    experiences = filter_by_title(
        Experience.objects.prefetch_related("starred_by"), title_query
    )

    data = []
    for experience in experiences:
        starred_users = experience.starred_by.all()
        is_starred = (
            request.user in starred_users if request.user.is_authenticated else False
        )

        data.append(
            {
                "pk": str(experience.id),
                "fields": {
                    "title": experience.title,
                    "description": experience.description,
                    "category": experience.category,
                    "thumbnail": experience.thumbnail,
                    "started_at": experience.started_at,
                    "ended_at": experience.ended_at,
                    "star_count": len(starred_users),
                    "is_starred": is_starred,
                    "starred_by_names": ", ".join(
                        user.username for user in starred_users
                    ),
                },
            },
        )

    return JsonResponse(data, safe=False)


def show_experiences(request):
    title_query = request.GET.get("title", "").strip()
    experiences = filter_by_title(Experience.objects.all(), title_query)

    context = {
        "name": NAME,
        "title_query": title_query,
        "is_editor": is_editor_user(request.user),
        "form": ExperienceForm(),
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


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add experiences."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience added successfully.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
