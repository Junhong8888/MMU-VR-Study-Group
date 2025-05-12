from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def datatables(request):
    return render(request, "datatables.html")

def dashboard(request):
    return render(request, "dashboard.html")

def home(request):
    return render(request, "home.html")