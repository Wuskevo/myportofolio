from django.urls import path

from main.views import show_main, show_experience, show_credential

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("credential/", show_credential, name="show_credential"),
]