from django.shortcuts import render

from main.models import Experience


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