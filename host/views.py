from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ClientForm, GuestLoginForm
from .models import Client
from django.contrib.auth.models import User
import random
import string

CustomUser = get_user_model()

def index(request):
    clients = Client.objects.all()
    return render(request, "host.html", {'clients': clients})

def generate_random_password():
    # Generate a random password of length 8
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@csrf_exempt
@login_required
def create_client(request):
    if not request.user.has_perm('accounts.can_create_client'):
        return HttpResponseBadRequest("You don't have permission to create clients.")
    
    clients = Client.objects.all()  # Define clients variable outside the if-else block

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
    # Set the user before saving the form
            client = form.save(commit=False)
            client.user = request.user  # You can directly assign the request.user
            client.save()
            password = generate_random_password()
            user = User.objects.create_user(username=client.email, password=password)
            print("clint username", client.username)
            print("Client after saving:", client.email)
            print("Client after saving:", client.phoneNumber)
            print("Client after saving:", client.rentPayDate)
            print("Client after saving:", client.rentEndDate)
            # print("pass", client.password)

            # Set the password directly on the User object
            user.set_password(password)
            user.save()
            print('Generated password:', password)
            # Refresh clients after saving new client
            clients = Client.objects.all()
        return render(request, 'host.html', {'clients': clients})
    else:
        form = ClientForm()
    return render(request, 'host.html', {'clients': clients, 'form': form})

@csrf_exempt
def guest_login(request):
    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                # Log in the user
                login(request, user)
                return redirect('/guest/')
            else:
                # Handle invalid credentials
                return render(request, 'guest_login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = GuestLoginForm()
    return render(request, 'guest_login.html', {'form': form})


# display all clients
def display_clients(request):
    clients = Client.objects.all()
    return render(request, 'host.html', {'clients': clients})

def display_clients(request):
    clients = Client.objects.all()
    return render(request, 'client.html', {'clients': clients})
@csrf_exempt
def delete_client(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect('create_client')