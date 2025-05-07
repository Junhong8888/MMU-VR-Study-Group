from django.shortcuts import render,redirect

# Create your views here.
def test_view(request):
    return render(request,'video.html',{})
