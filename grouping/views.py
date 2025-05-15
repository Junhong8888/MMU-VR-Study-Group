from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Room
from .forms import GroupForm,JoinCodeForm

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
        
        elif form_type == 'join_group':
            group_code = request.POST.get('group_code')

            try:
                # Validate the group code and add the user to the room
                room = Room.objects.get(group_code=group_code)
                room.members.add(request.user)
                return redirect('chat:room', room_name=room.roomname)
            except Room.DoesNotExist:
                return render(request, 'room.html', {
                    'topics': topics,
                    'error': 'Invalid group code. Please try again.',
                })

    context = {
        'topics': topics,
    }
    return render(request, 'room.html', context)


@login_required
def join_group(request):
    error = None

    if request.method == 'POST':
        group_code = request.POST.get('group_code')  # Get the group code submitted by the user

        if not group_code:
            error = "Group code is required to join a group."
        else:
            try:
                # Validate the group code
                room = Room.objects.get(join_code=group_code)  # Ensure group_code is unique in the model
                # Add the logged-in user to the room
                room.members.add(request.user)
                return redirect('chat:room', room_name=room.roomname)
            except Room.DoesNotExist:
                error = "Invalid group code. Please try again."

    return render(request, 'join_by_code.html', {'error': error})

@login_required
def host_workspace(request, room_id):
    group = get_object_or_404(Room, id=room_id)

    # Check if user is host or member
    if request.user == group.host or request.user in group.members.all():
        return render(request, 'group/host_workspace.html', {'group': group})
    else:
        return redirect('home')  # or show a permission denied message