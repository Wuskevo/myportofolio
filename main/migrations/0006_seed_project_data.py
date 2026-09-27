from django.db import migrations


def seed_project_data(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    projects = [
        {
            "title": "Nabla's Ascent",
            "description": "Ascend a dark tower full of killer robots.",
            "tech_stack": "Godot, 2D, Shooter, Platformer, Roguelike",
            "project_url": "https://htsdfisy.itch.io/nablas-ascent",
            "project_image_url": "https://img.itch.zone/aW1nLzI5NDczNTQ1LnBuZw==/315x250%23c/UePDYD.png",
        },
        {
            "title": "Red's Elemental Duel",
            "description": "Trigger chaotic elemental chain reactions upon golem mayhem.",
            "tech_stack": "Godot, 2D, Puzzle, Arcade",
            "project_url": "https://aksaindo1834.itch.io/reds-elemental-duel",
            "project_image_url": "https://img.itch.zone/aW1nLzI5NzYzMTA3LnBuZw==/315x250%23c/GVVsQG.png",
        },
    ]
    database = schema_editor.connection.alias

    for project_data in projects:
        project, created = Project.objects.using(database).get_or_create(
            title=project_data["title"],
            defaults=project_data,
        )
        if created:
            continue

        missing_values = {
            field: project_data[field]
            for field in ("project_url", "project_image_url")
            if not getattr(project, field) and project_data[field]
        }
        if missing_values:
            Project.objects.using(database).filter(pk=project.pk).update(**missing_values)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_seed_home_projects"),
    ]

    operations = [
        migrations.RunPython(seed_project_data, migrations.RunPython.noop),
    ]