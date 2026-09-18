from django.urls import path

from main.views import (
    create_credentials,
    create_experience,
    delete_credentials,
    delete_experience,
    get_credentials_json,
    show_main,
    show_credentials,
    show_experience,
    update_credentials,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("credentials/", show_credentials, name="show_credentials"),
	path("credentials/json/", get_credentials_json, name="get_credentials_json"),
	path("experience/add/", create_experience, name="create_experience"),
	path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("credentials/add/", create_credentials, name="create_credentials"),
    path(
        "credentials/<uuid:credential_id>/edit/",
        update_credentials,
        name="update_credentials",
    ),
    path(
        "credentials/<uuid:credential_id>/delete/",
        delete_credentials,
        name="delete_credentials",
    ),
]