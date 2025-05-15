from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserSession
from django.utils.timezone import now

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    UserSession.objects.create(user=user, login_time=now())

@receiver(user_logged_out)
def on_user_logout(sender, request, user, **kwargs):
    try:
        session = UserSession.objects.filter(user=user, logout_time__isnull=True).latest('login_time')
        session.logout_time = now()
        session.save()
    except UserSession.DoesNotExist:
        pass
