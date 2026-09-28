NAME = "Clement Kevin Tanadi"
NPM = "2506632892"
STUDY_PROGRAM = "Undergrad Computer Science"
BIO = (
    "CS student at Universitas Indonesia passionate in Game Development and Competitive Programming."
    "Currently working on indie games joining jams and competitions."
)

EDITOR_STR = "Editor"


def is_editor_user(user):
    return user.is_authenticated and user.groups.filter(name=EDITOR_STR).exists()


def filter_by_title(queryset, title_query):
    if title_query:
        return queryset.filter(title__icontains=title_query)
    return queryset