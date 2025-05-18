from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Room
from .forms import GroupForm,JoinCodeForm
from zfeng.models import todo
from zfeng.forms import TodoForm

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

            return redirect('workspace',Room_join_code=room.join_code)
        
        elif form_type == 'join_group':
            group_code = request.POST.get('group_code')

            try:
                # Validate the group code and add the user to the room
                room = Room.objects.get(group_code=group_code)
                room.members.add(request.user)
                return redirect('workspace')
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
        group_code = request.POST.get('join_code')  # Get the group code submitted by the user

        if not group_code:
            error = "Group code is required to join a group."
        else:
            try:
                # Validate the group code
                room = Room.objects.get(join_code=group_code)  # Ensure group_code is unique in the model
                # Add the logged-in user to the room
                room.members.add(request.user)
                #return redirect('chat:room', room_name=room.roomname)
                return redirect('workspace',Room_join_code=room.join_code)
            except Room.DoesNotExist:
                error = "Invalid group code. Please try again."

    return render(request, 'join_by_code.html', {'error': error})

'''
@login_required
def workspace(request, room_id):
    group = get_object_or_404(Room, id=room_id)

    # Check if user is host or member
    if request.user == group.host or request.user in group.members.all():
        return render(request, 'todo.html', {'group': group})
    else:
        return redirect('home')  # or show a permission denied message
'''

@login_required
def workspace(request, Room_join_code):
    workspace = get_object_or_404(Room, join_code=Room_join_code)

    # Ensure the user is part of the room
    if not (request.user == workspace.host or request.user in workspace.members.all()):
        return redirect('home')

    # Handle task creation
    if request.method == 'POST':
        task_name = request.POST.get('task')
        if task_name:
            todo.objects.create(
                user=request.user,
                todo_name=task_name,
                workspace=workspace  # This links the task to the current workspace
            )
            return redirect('workspace', Room_join_code=Room_join_code)

    tasks = todo.objects.filter(workspace=workspace)

    return render(request, "workspace.html", {
        "workspace": workspace,
        "tasks": tasks
    })



def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('todolist')


def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('todolist')

def TaskDetail(request, name):
    task = todo.objects.get(user=request.user, todo_name=name)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todolist')
    else:
        form = TodoForm(instance=task)

    return render(request, 'task_detail.html', {'form': form, 'task': task})
