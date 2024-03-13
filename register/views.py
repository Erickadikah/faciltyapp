from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages

@login_required # This is a custom decorator
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # You don't need to authenticate the user after registration,
            # because the user is already created and authenticated by the save() method
            login(request, user)
            return redirect("/login/")  # Redirect to login page or any other page after registration
        else:
            # Display error messages if the form is invalid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/guest/")
    return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

def user_list(request):
    users = User.objects.all()
    print(users)
    return render(request, "host.html", {"users": users})