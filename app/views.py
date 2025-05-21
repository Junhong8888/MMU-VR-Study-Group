from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserSession
from django.db.models import Count
import json
from datetime import timedelta

@login_required
def index(request):
    # Get all sessions for the logged-in user
    sessions = UserSession.objects.filter(user=request.user)

    # Calculate usage per day in minutes
    usage_per_day = {}
    for session in sessions:
        if session.logout_time and session.login_time:
            day = session.login_time.date()
            minutes = (session.logout_time - session.login_time).total_seconds() / 60
            usage_per_day[day] = usage_per_day.get(day, 0) + round(minutes, 2)

    today = timezone.now().date()
    minutes_today = usage_per_day.get(today, 0)

    # Count distinct users who logged in today
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    total_users_today = UserSession.objects.filter(
        login_time__gte=today_start, login_time__lt=today_end
    ).values('user').distinct().count()

    # Chart data: number of users who logged in per day over the last 7 days
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    user_count_per_day = {}

    for day in last_7_days:
        day_start = timezone.make_aware(timezone.datetime.combine(day, timezone.datetime.min.time()))
        day_end = day_start + timedelta(days=1)
        count = UserSession.objects.filter(login_time__gte=day_start, login_time__lt=day_end).values('user').distinct().count()
        user_count_per_day[day.strftime('%b %d')] = count

    chart_labels = json.dumps(list(user_count_per_day.keys()))
    chart_data = json.dumps(list(user_count_per_day.values()))

    context = {
        'minutes_today': round(minutes_today, 2),
        'total_users_today': total_users_today,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }

    return render(request, 'dashboard.html', context)

@login_required
def home(request):
    return render(request, 'home.html')
