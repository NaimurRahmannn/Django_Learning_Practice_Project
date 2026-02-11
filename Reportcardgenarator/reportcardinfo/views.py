from django.shortcuts import render, redirect
from .forms import StudentForm
from django.contrib import messages
from .models import Student
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
@login_required(login_url='login')
def student_info(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student=form.save()
            messages.success(request, 'Student info add successfully')
            return redirect("student_info")
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {"form": form})

@login_required(login_url='login')
def report_card(request):
    students = Student.objects.all()
    return render(request, 'report_card.html', {"students": students})

def registration(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('registration')
        user=User.objects.create_user(
            username=username,
            password=password
        )
        user.save()
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    return render(request, 'signup.html')

def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('student_info')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')
