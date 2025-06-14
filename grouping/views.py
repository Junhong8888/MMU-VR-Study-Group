from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Room
from .forms import GroupForm,JoinCodeForm,TaskForm
from zfeng.models import todo
from django.contrib.auth.models import User
from datetime import datetime
from .models import Document
from .forms import DocumentForm
from django.http import HttpResponseForbidden
from django.db.models import Count



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

            return redirect('grouping:workspace',Room_join_code=room.join_code)
        
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
                return redirect('grouping:workspace',Room_join_code=room.join_code)
            except Room.DoesNotExist:
                error = "Invalid group code. Please try again."

    return render(request, 'join_by_code.html', {'error': error})


@login_required
def workspace(request, Room_join_code):
    workspace = get_object_or_404(Room, join_code=Room_join_code)
    user_rooms = Room.objects.filter(members=request.user)

    # Ensure user is part of the room
    if not (request.user == workspace.host or request.user in workspace.members.all()):
        return redirect('home')

    # Handle task creation
    if request.method == 'POST':
        task_name = request.POST.get('task')
        assigned_to_id = request.POST.get('assigned_to')
        due_date_str = request.POST.get('due_date')

        if task_name:
            assigned_user = User.objects.get(id=assigned_to_id) if assigned_to_id else None
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

            todo.objects.create(
                user=request.user,
                todo_name=task_name,
                assigned_to=assigned_user,
                due_date=due_date,
                workspace=workspace
            )
            return redirect('grouping:workspace', Room_join_code=Room_join_code)

    tasks = todo.objects.filter(workspace=workspace)
    members = workspace.members.all()


    return render(request, "workspace.html", {
        "workspace": workspace,
        "tasks": tasks,
        "user_rooms": user_rooms,
        "members": members,  
    })



def DeleteTask(request, id):
    get_todo = get_object_or_404(todo, id=id)
    if request.user not in get_todo.workspace.members.all():
        return HttpResponseForbidden("You do not have permission to delete this task.")
    room_code = get_todo.workspace.join_code
    get_todo.delete()
    return redirect('grouping:workspace', Room_join_code=room_code)


def Update(request, id):
    get_todo = get_object_or_404(todo, id=id)
    if request.user not in get_todo.workspace.members.all():
        return HttpResponseForbidden("You do not have permission to delete this task.")
    get_todo.status = True
    get_todo.save()
    return redirect('grouping:workspace',Room_join_code=get_todo.workspace.join_code)

def TaskDetail(request, id):
    task = get_object_or_404(todo, id=id,)
    if request.user not in task.workspace.members.all():
        return HttpResponseForbidden("You do not have permission to delete this task.")
    workspace = task.workspace

    # Ensure document exists
    if task.document is None:
        document = Document.objects.create(title=f'Document for task {task.todo_name}')
        task.document = document
        task.save()
    else:
        document = task.document

    if request.method == 'POST':
        todo_form = TaskForm(request.POST, instance=task, workspace=workspace, prefix="task")
        doc_form = DocumentForm(request.POST, request.FILES, instance=document, prefix="doc")

        if todo_form.is_valid() and doc_form.is_valid():
            todo_form.save()
            doc_form.save()
            return redirect('grouping:workspace', Room_join_code=workspace.join_code)
    else:
        todo_form = TaskForm(instance=task, workspace=workspace, prefix="task")
        doc_form = DocumentForm(instance=document, prefix="doc")

    return render(request, 'task_detail.html', {
        'todo_form': todo_form,
        'doc_form': doc_form,
        'task': task,
        'document': document,
    })

@login_required
def ranking(request, Room_join_code):
    workspace = get_object_or_404(Room, join_code=Room_join_code)

    # Ensure user is part of the room
    if not (request.user == workspace.host or request.user in workspace.members.all()):
        return redirect('home')

    members = workspace.members.all()

    ranking = (
        todo.objects.filter(workspace=workspace, status=True, assigned_to__in=members)
        .values('assigned_to__username')
        .annotate(completed_count=Count('id'))
        .order_by('-completed_count')
    )

    return render(request, "ranking.html", {
        "workspace": workspace,
        "ranking": ranking
    })

