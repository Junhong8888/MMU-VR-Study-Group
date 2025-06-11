from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserSession
from django.utils.timezone import now

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    UserSession.objects.create(
        user=user,
        session_key=request.session.session_key,
        login_time=now()
    )

@receiver(user_logged_out)
def on_user_logout(sender, request, user, **kwargs):
    session_key = request.session.session_key
    try:
        session = UserSession.objects.get(user=user, session_key=session_key, logout_time__isnull=True)
        session.logout_time = now()
        session.duration_minutes = int((session.logout_time - session.login_time).total_seconds() // 60)
        session.save()
    except UserSession.DoesNotExist:
        pass