from django.db import migrations


def seed_home_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    database = schema_editor.connection.alias
    projects = [
        {
            "title": "Nabla's Ascent",
            "description": "Ascend a dark tower full of killer robots.",
            "tech_stack": "Godot, 2D, Shooter, Platformer, Roguelike",
            "project_url": "https://htsdfisy.itch.io/nablas-ascent",
            "project_image_url": "",
        },
        {
            "title": "Red's Elemental Duel",
            "description": "Trigger chaotic elemental chain reactions upon golem mayhem.",
            "tech_stack": "Godot, 2D, Puzzle, Arcade",
            "project_url": "https://aksaindo1834.itch.io/reds-elemental-duel",
            "project_image_url": "",
        },
    ]

    for project in projects:
        Project.objects.using(database).get_or_create(
            title=project["title"],
            defaults=project,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_project"),
    ]

    operations = [
        migrations.RunPython(seed_home_projects, migrations.RunPython.noop),
    ]