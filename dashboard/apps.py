from django.apps import AppConfig

<<<<<<< HEAD
=======


>>>>>>> deploy
class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
<<<<<<< HEAD
        import dashboard.signals
=======
        try:
            import dashboard.signals
        except Exception as e:
            print("Error importing signals:", e)
>>>>>>> deploy
