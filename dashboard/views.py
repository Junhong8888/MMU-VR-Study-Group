from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserSession
from django.db.models import Count
import json
from datetime import timedelta, datetime
from collections import defaultdict
from zfeng.models import todo

def split_session_across_days(session, now):
    """Returns a dict: {date: minutes_used_on_that_date} for the given session."""
    usage = defaultdict(float)
    start = session.login_time
    end = session.logout_time or now
    current = start

    while current.date() <= end.date():
        day_start = timezone.make_aware(datetime.combine(current.date(), datetime.min.time()))
        day_end = day_start + timedelta(days=1)
        period_start = max(start, day_start)
        period_end = min(end, day_end)
        if period_start < period_end:
            usage[current.date()] += (period_end - period_start).total_seconds() / 60
        current += timedelta(days=1)
    return usage

@login_required
def index(request):
    now = timezone.now()
    today = now.date()

    # Get all sessions for the logged-in user
    sessions = UserSession.objects.filter(user=request.user)

    # Calculate usage per day (including sessions spanning multiple days)
    usage_per_day = defaultdict(float)
    for session in sessions:
        split_usage = split_session_across_days(session, now)
        for day, minutes in split_usage.items():
            usage_per_day[day] += round(minutes, 2)

    minutes_today = round(usage_per_day.get(today, 0), 2)

    # Count distinct users who logged in today
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = today_start + timedelta(days=1)
    total_users_today = UserSession.objects.filter(
        login_time__gte=today_start,
        login_time__lt=today_end
    ).values('user').distinct().count()

    # Chart data: total usage time per day (minutes) for all users over the last 7 days
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    usage_per_day_all = defaultdict(float)
    all_sessions = UserSession.objects.all()
    for session in all_sessions:
        split_usage = split_session_across_days(session, now)
        for day, minutes in split_usage.items():
            usage_per_day_all[day] += round(minutes, 2)

    chart_labels = []
    chart_data = []
    for day in last_7_days:
        chart_labels.append(day.strftime('%b %d'))
        chart_data.append(round(usage_per_day_all.get(day, 0), 2))

    # Last login time of the user
    last_login = request.user.last_login
    user_last_login = timezone.localtime(last_login).strftime('%Y-%m-%d %H:%M:%S') if last_login else "Never logged in"

    context = {
        'minutes_today': minutes_today,
        'total_users_today': total_users_today,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'task_count': todo.objects.filter(user=request.user).count(),
        'user_last_login': user_last_login
    }

    return render(request, 'dashboard.html', context)

@login_required
def home(request):
    return render(request, 'home.html')
