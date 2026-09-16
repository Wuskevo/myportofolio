from django.urls import path

from main.views import show_main, show_experience, show_credential, create_experience, delete_experience

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("credential/", show_credential, name="show_credential"),
	path("experience/add/", create_experience, name="create_experience"),
	path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience")
]