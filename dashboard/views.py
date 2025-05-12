from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "dashboard.html")

def home(request):
    return render(request, "home.html")

def reports(request):
    return render(request, "reports.html")
