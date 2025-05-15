from django.shortcuts import render
from .models import UserSession
from django.contrib.auth.decorators import login_required
from django.utils import timezone  # Needed to get current date

def datatables(request):
    return render(request, 'dashboard.html')

def home(request):
    return render(request, 'home.html')

@login_required
def index(request):
    # Fetch sessions for the current user
    sessions = UserSession.objects.filter(user=request.user)

    # Calculate total hours used per day
    usage_per_day = {}
    for session in sessions:
        if session.logout_time and session.login_time:
            day = session.login_time.date()
            hours = (session.logout_time - session.login_time).total_seconds() / 3600
            usage_per_day[day] = usage_per_day.get(day, 0) + round(hours, 2)

    # Get today's date and fetch usage for today
    today = timezone.now().date()
    hours_today = usage_per_day.get(today, 0)

    context = {
        'usage_per_day': usage_per_day,  # Optional: for charting or future use
        'hours_today': hours_today,      # Used in your template
    }

    return render(request, 'dashboard.html', context)
