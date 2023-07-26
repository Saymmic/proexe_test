from django.apps import AppConfig


class DynamicTablesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "proexe.dynamic_tables"

    def ready(self):
        try:
            import proexe.users.signals  # noqa: F401
        except ImportError:
            pass
