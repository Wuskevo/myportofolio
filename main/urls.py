from django.urls import path

from main.views import (
    create_credentials,
    create_experiences,
    delete_credentials,
    delete_experiences,
    get_credentials_json,
    get_experiences_json,
    show_main,
    show_credentials,
    show_experiences,
    update_credentials,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experiences, name="show_experiences"),
    path("experiences/json/", get_experiences_json, name="get_experiences_json"),
    path("credentials/", show_credentials, name="show_credentials"),
	path("credentials/json/", get_credentials_json, name="get_credentials_json"),
    path("experiences/add/", create_experiences, name="create_experiences"),
    path("experiences/<uuid:experience_id>/delete/", delete_experiences, name="delete_experiences"),
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