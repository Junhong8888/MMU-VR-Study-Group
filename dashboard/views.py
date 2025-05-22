from django.shortcuts import render
from zfeng.models import todo  # import Task model from todo app
from .models import UserSession
from django.contrib.auth.decorators import login_required
from django.utils import timezone  # Needed to get current date

def index(request):
    task_count = todo.objects.count()  # Get total number of tasks
    return render(request, 'dashboard.html', {'task_count': task_count})


def home(request):
    return render(request, "home.html")


def reports(request):
    return render(request,"reports.html")


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
            hours = (session.logout_time - session.login_time).total_seconds() 
            usage_per_day[day] = usage_per_day.get(day, 0) + round(hours, 2)

    # Get today's date and fetch usage for today
    today = timezone.now().date()
    hours_today = usage_per_day.get(today, 0)

    context = {
        'usage_per_day': usage_per_day,  
        'hours_today': hours_today,
        'task_count' : todo.objects.filter(user=request.user).count()  # Get total number of tasks      
    }

    return render(request, 'dashboard.html', context)