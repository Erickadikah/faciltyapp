from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        # print("form: ", form)
        if form.is_valid():
            user = form.save()
            print("user: ", user)
            print("username", user.username)
            print("password", user.password)
            print("email", user.email)
            # print("phone", user.phone)
            print("address", user.address)
            print("eircode", user.eircode)
            print("country", user.country)
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
            return redirect("/host/")
    return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

def user_list(request):
    users = User.objects.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # 'phone': user.phone,
            # 'address': user.address,
            # 'eircode': user.eircode,
            # 'country': user.country,
            # Add more fields as needed
        }
        user_list.append(user_data)
    return JsonResponse(user_list, safe=False)

# user with user id
def user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # 'phone': user.phone,
            # Add more fields as needed
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)