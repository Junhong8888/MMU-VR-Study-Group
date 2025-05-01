from django.shortcuts import render
from django.http import HttpResponse

#request handler 

def say_hello(request):
    return render(request,'caller.html',{})
