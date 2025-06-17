from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserSession
import json
from datetime import timedelta, datetime
from collections import defaultdict
from zfeng.models import todo

def get_minutes_today(user):
    now = timezone.localtime(timezone.now())
    today = now.date()
    sessions = UserSession.objects.filter(user=user)
    usage_per_day = defaultdict(float)
    for session in sessions:
        split_usage = split_session_across_days(session, now)
        for day, minutes in split_usage.items():
            usage_per_day[day] += round(minutes, 2)
    return round(usage_per_day.get(today, 0), 2)

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
<<<<<<< HEAD
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
=======
    now = timezone.localtime(timezone.now())  # always current local time
    today = now.date()
    sessions = UserSession.objects.filter(user=request.user)

    usage_per_day = defaultdict(float)
    for session in sessions:
        split_usage = split_session_across_days(session, now)
        for day, minutes in split_usage.items():
            usage_per_day[day] += round(minutes, 2)

    minutes_today = round(usage_per_day.get(today, 0), 2)

    # Count distinct users who logged in today
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
>>>>>>> deploy
    today_end = today_start + timedelta(days=1)
    total_users_today = UserSession.objects.filter(
        login_time__gte=today_start,
        login_time__lt=today_end
    ).values('user').distinct().count()

    # Chart data: total usage time per day (minutes) for all users over the last 7 days
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
<<<<<<< HEAD
    usage_per_day_all = {}
=======
    usage_per_day_user = defaultdict(float)
    user_sessions = UserSession.objects.filter(user=request.user)
    for session in user_sessions:
        split_usage = split_session_across_days(session, now)
        for day, minutes in split_usage.items():
            usage_per_day_user[day] += round(minutes, 2)
>>>>>>> deploy

    chart_labels = []
    chart_data = []
    for day in last_7_days:
<<<<<<< HEAD
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

=======
        chart_labels.append(day.strftime('%b %d'))
        chart_data.append(round(usage_per_day_user.get(day, 0), 2))
        
>>>>>>> deploy
    # Last login time of the user
    last_login = request.user.last_login
    user_last_login = timezone.localtime(last_login).strftime('%Y-%m-%d %H:%M:%S') if last_login else "Never logged in"

    context = {
        'minutes_today': minutes_today,
        'total_users_today': total_users_today,
<<<<<<< HEAD
        'chart_labels': chart_labels,
        'chart_data': chart_data,
=======
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
>>>>>>> deploy
        'task_count': todo.objects.filter(user=request.user).count(),
        'user_last_login': user_last_login
    }

    return render(request, 'dashboard.html', context)

@login_required
def home(request):
    return render(request, 'home.html')
