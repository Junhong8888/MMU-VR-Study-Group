from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
<<<<<<< HEAD
from your_project.models import Workspace  # Adjust this import path accordingly

@login_required
def load_messages(request, workspace_id):
    try:
        workspace = Workspace.objects.get(id=workspace_id)
    except Workspace.DoesNotExist:
=======
from grouping.models import Room  # Adjust this import path accordingly

@login_required
def load_messages(request, room_id):
    try:
        workspace = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
>>>>>>> deploy
        return JsonResponse({'error': 'Workspace not found'}, status=404)

    messages = ChatMessage.objects.filter(workspace=workspace).order_by('timestamp')
    data = [{
        'user': msg.user.username,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
    } for msg in messages]

    return JsonResponse(data, safe=False)
