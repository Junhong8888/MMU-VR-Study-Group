from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
from .forms import TodoForm , TaskForm , DocumentForm
from grouping.models import Document

# Create your views here.


def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        if task:
            new_todo = todo(user=request.user, todo_name=task)
            new_todo.save()
        return redirect('zfeng:todolist')  # 👈 redirect to clear POST

    all_todos = todo.objects.filter(user=request.user, workspace=None)
    context = {
        'todos': all_todos
    }
    return render(request, 'todo.html', context)



def DeleteTask(request, id):
    get_todo = get_object_or_404(todo, user=request.user, id=id)
    get_todo.delete()
    return redirect('zfeng:todolist')


def Update(request, id):
    get_todo = get_object_or_404(todo, user=request.user, id=id)
    get_todo.status = True
    get_todo.save()
    return redirect('zfeng:todolist')

def TaskDetail(request, id):
    task = get_object_or_404(todo, id=id,)
    

    # Ensure document exists
    if task.document is None:
        document = Document.objects.create(title=f'Document for task {task.todo_name}')
        task.document = document
        task.save()
    else:
        document = task.document

    if request.method == 'POST':
        todo_form = TodoForm(request.POST, instance=task,  prefix="task")
        doc_form = DocumentForm(request.POST, request.FILES, instance=document, prefix="doc")

        if todo_form.is_valid() and doc_form.is_valid():
            todo_form.save()
            doc_form.save()
            return redirect('zfeng:todolist')
    else:
        todo_form = TodoForm(instance=task,  prefix="task")
        doc_form = DocumentForm(instance=document, prefix="doc")

    return render(request, 'task_detail.html', {
        'todo_form': todo_form,
        'doc_form': doc_form,
        'task': task,
        'document': document,
    })



