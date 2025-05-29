from .models import Room

def user_workspaces(request):
    if request.user.is_authenticated:
        rooms = Room.objects.filter(members=request.user).exclude(join_code__isnull=True).exclude(join_code__exact='')
        return {'user_rooms': rooms}
    return {}
