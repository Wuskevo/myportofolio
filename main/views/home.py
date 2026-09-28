from django.shortcuts import render

from main.models import Project

from .common import BIO, NAME, NPM, STUDY_PROGRAM, is_editor_user


def show_main(request):
    last_login = request.COOKIES.get("last_login", "No active login session / Cookie not found")
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