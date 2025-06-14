from django.shortcuts import render , redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.
def home(request):
    return render(request,'base.html')

def login_signup(request):
    signup_form = SignUpForm()  

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('zfeng:todolist')  
            else:
                messages.error(request, 'Invalid username or password.')

        elif form_type == 'signup':
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('home')  
            else:
                print(signup_form.errors)

    return render(request, 'mmu proj.html', {'form': signup_form})

def main(request):
    return render(request,'main.html')

def user_logout(request):
    logout(request)
    return redirect('home')


