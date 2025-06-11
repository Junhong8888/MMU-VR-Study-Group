from django.apps import AppConfig



class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        try:
            import dashboard.signals
        except Exception as e:
            print("Error importing signals:", e)
