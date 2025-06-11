from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserSession
from django.db.models import Count
import json
from datetime import timedelta
from zfeng.models import todo

@login_required
def index(request):
   now = timezone.now()
   today = now.date()

    # Get all sessions for the logged-in user
   sessions = UserSession.objects.filter(user=request.user)

    # Calculate usage per day in minutes, including active sessions
   usage_per_day = {}

   for session in sessions:
        if session.login_time:
            session_day = session.login_time.date()
            end_time = session.logout_time or now  # Use current time if session still active
            duration = (end_time - session.login_time).total_seconds() / 60
            usage_per_day[session_day] = usage_per_day.get(session_day, 0) + round(duration, 2)

   minutes_today = usage_per_day.get(today, 0)

    # Count distinct users who logged in today
   today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
   today_end = today_start + timedelta(days=1)

   total_users_today = UserSession.objects.filter(
        login_time__gte=today_start,
        login_time__lt=today_end
    ).values('user').distinct().count()

    # Chart data: total usage time per day (minutes) for all users over the last 7 days
   last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
   usage_per_day_all = {}

   for day in last_7_days:
        day_start = timezone.make_aware(timezone.datetime.combine(day, timezone.datetime.min.time()))
        day_end = day_start + timedelta(days=1)
        sessions_in_day = UserSession.objects.filter(
            login_time__gte=day_start,
            login_time__lt=day_end
        )

        total_seconds = 0
        for s in sessions_in_day:
            end_time = s.logout_time or now
            duration = (end_time - s.login_time).total_seconds()
            total_seconds += duration

        usage_per_day_all[day.strftime('%b %d')] = round(total_seconds / 60, 2)  # convert to minutes

   chart_labels = json.dumps(list(usage_per_day_all.keys()))
   chart_data = json.dumps(list(usage_per_day_all.values()))

    # Last login time of the user
   last_login = request.user.last_login
   user_last_login = timezone.localtime(last_login).strftime('%Y-%m-%d %H:%M:%S') if last_login else "Never logged in"

   context = {
        'minutes_today': round(minutes_today, 2),
        'total_users_today': total_users_today,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'task_count': todo.objects.filter(user=request.user).count(),
        'user_last_login': user_last_login
    }

   return render(request, 'dashboard.html', context)


@login_required
def home(request):
    return render(request, 'home.html')
