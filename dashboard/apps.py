from django.apps import AppConfig

print("dashboard.signals has been imported!")

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        print("DashboardConfig.ready() called")
        try:
            import dashboard.signals
        except Exception as e:
            print("Error importing signals:", e)
