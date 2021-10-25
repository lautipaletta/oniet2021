from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
import requests

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    return render(request, 'dashboard.html', {})

def login(request):
    
    if request.method == 'POST':
        
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user:

            auth_login(request, user)

            return redirect('index')

        else:
            return render(request, 'login.html', {'error_message': 'El email o el usuario ingresados son incorrectos.'})

    else:
        return render(request, 'login.html', {})

    
    if request.method == 'POST':
        
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return HttpResponse('Por favor, complete todos los campos.')

    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')