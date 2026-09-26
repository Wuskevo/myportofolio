from django.urls import path

from main.views import (
    
    create_credential,
    create_experience,
    create_project,
    
    get_credentials_json,
    get_experiences_json,
    get_projects_json,
    
    show_main,
    show_credentials,
    show_experiences,
    show_projects,
    
    update_experience,
    update_credential,
    update_project,
    
    delete_credential,
    delete_experience,
    delete_project,
    
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
	
    path("credentials/add/", create_credential, name="create_credential"),
   	path("credentials/json/", get_credentials_json, name="get_credentials_json"), 
    path("credentials/", show_credentials, name="show_credentials"),
    path(
        "credentials/<uuid:credential_id>/edit/",
        update_credential,
        name="update_credential",
    ),
    path(
        "credentials/<uuid:credential_id>/delete/",
        delete_credential,
        name="delete_credential",
    ),
    
    path("experiences/add/", create_experience, name="create_experience"),
    path("experiences/", show_experiences, name="show_experiences"),
	path("experiences/json/", get_experiences_json, name="get_experiences_json"),	
    path(
        "experiences/<uuid:experience_id>/edit/",
        update_experience,
        name="update_experience",
    ),
    path("experiences/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    
    path("projects/add/", create_project, name="create_project"),
	path("projects/", show_projects, name="show_projects"),
	path("projects/json/", get_projects_json, name="get_projects_json"),	
	path(
		"projects/<uuid:project_id>/edit/",
		update_project,
		name="update_project",
	),
	path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
]