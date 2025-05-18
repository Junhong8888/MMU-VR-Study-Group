from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        if task: 
            new_todo = todo(user=request.user, todo_name=task)
            new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todo.html', context)



@login_required
def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')

@login_required
def TaskDetail(request, name):
    task = todo.objects.get(user=request.user, todo_name=name)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home-page')
    else:
        form = TodoForm(instance=task)

    return render(request, 'todoapp/task_detail.html', {'form': form, 'task': task})

def reset_password(request):
    return render(request, 'todoapp/reset_password.html') 