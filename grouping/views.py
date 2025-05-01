from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Room
from .forms import GroupForm

def group(request): 
    return render(request,'room.html',{})


@login_required
def createRoom(request):
    topics = Topic.objects.all()

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        
        if form_type == 'create_group':
            topic_name = request.POST.get('topic')
            roomname = request.POST.get('roomname')
            description = request.POST.get('description')

            topic, created = Topic.objects.get_or_create(name=topic_name)

            room = Room.objects.create(
                host=request.user,
                roomname=roomname,
                description=description,
                topic=topic
            )

            room.members.add(request.user)

            return redirect('chat:room', room_name = roomname)

    context = {
        'topics': topics,
    }
    return render(request, 'room.html', context)