from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.

def login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('db')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')

def register(request):

    if request.method == 'POST':

        name = request.POST['first_name']
        surname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        if password == password_confirmation and password !="":
            #checking if user name exists
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'E-mail Taken')
                return redirect('register')
            else:
                #creating the user in order to keep all the information into the database
                user = User.objects.create_user(username=username,password=password,email=email,first_name=name,last_name=surname)
                user.save()
                return redirect('/')
        else:
            messages.info(request, "Passwords don't match or empty Password field")
            return redirect('register')

    else:
        return render(request, 'register.html')