from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.models'

    def ready(self):
        from .projects import Project
        from .meets import Meet

