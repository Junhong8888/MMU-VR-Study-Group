from django.apps import AppConfig


class WorkspaceChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workspace_chat'
<<<<<<< HEAD
=======

    def ready(self):
        import workspace_chat.signals
>>>>>>> deploy
