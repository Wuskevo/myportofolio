from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import CredentialForm
from main.models import Credential

from .common import NAME, filter_by_title, is_editor_user


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
    credentials = filter_by_title(
        Credential.objects.prefetch_related("starred_by"), title_query
    )

    data = []
    for credential in credentials:
        starred_users = list(credential.starred_by.all())
        data.append(
            {
                "pk": str(credential.id),
                "fields": {
                    "title": credential.title,
                    "description": credential.description,
                    "category": credential.category,
                    "issuer": credential.issuer,
                    "date_received": credential.date_received,
                    "expiry_date": credential.expiry_date,
                    "credential_url": credential.credential_url,
                    "image": credential.image.url if credential.image else None,
                    "star_count": len(starred_users),
                    "is_starred": (
                        request.user in starred_users
                        if request.user.is_authenticated
                        else False
                    ),
                    "starred_by_names": ", ".join(
                        user.username for user in starred_users
                    ),
                },
            }
        )

    return JsonResponse(data, safe=False)


def show_credentials(request):
    title_query = request.GET.get("title", "").strip()
    credentials = filter_by_title(
        Credential.objects.prefetch_related("starred_by"), title_query
    )
    credentials_by_category = {}
    for credential in credentials:
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


@login_required(login_url="/login/")
@require_POST
def toggle_credential_star(request, credential_id):
    credential = get_object_or_404(Credential, pk=credential_id)

    if request.user in credential.starred_by.all():
        credential.starred_by.remove(request.user)
    else:
        credential.starred_by.add(request.user)

    return redirect("main:show_credentials")