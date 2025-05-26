from django.shortcuts import render,redirect



# Create your views here.
def index(request):
    return render(request,'base.html',{})

def room(request,room_name):
    return render(request,'chatroom.html',{
        'room_name': room_name
    })

def etherpad(request):
    return render(request,'pad_embed.html',{})