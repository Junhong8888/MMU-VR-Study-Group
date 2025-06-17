from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from .forms import DocumentForm
# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        if task: 
            new_todo = todo(user=request.user, todo_name=task)
            new_todo.save()

    all_todos = todo.objects.all()
    all_documents = Document.objects.all()

    context = {
        'todos': all_todos,
        'documents': all_documents
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists, User another.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')


    return render(request, 'todoapp/login.html', {})

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

def document_edit(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    form = DocumentForm(request.POST or None, instance=doc)
    if form.is_valid():
        form.save()
        return redirect('document_list')
    return render(request, 'todoapp/document_form.html', {'form': form}) 

def document_list(request):
    docs = Document.objects.all()
    return render(request, 'todoapp/document_list.html', {'documents': docs})

def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.save()
            return redirect('home-page')
    else:
        form = DocumentForm()
    return render(request, 'todoapp/document_form.html', {'form': form})