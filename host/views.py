from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ClientForm, GuestLoginForm
from .models import Client

CustomUser = get_user_model()

def index(request):
    clients = Client.objects.all()
    return render(request, "host.html", {'clients': clients})

@csrf_exempt
@login_required
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
            print("Client after saving:", client.email)
            print("Client after saving:", client.phoneNumber)
            print("Client after saving:", client.rentPayDate)
            print("Client after saving:", client.rentEndDate)
            # Refresh clients after saving new client
            clients = Client.objects.all()
        return render(request, 'host.html', {'clients': clients})
    else:
        form = ClientForm()
    return render(request, 'host.html', {'clients': clients, 'form': form})


def guest_login(request):
    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                if user.has_perm('accounts.can_login_as_guest'):
                    # Log in the user
                    login(request, user)
                    return redirect('/guest/')
                else:
                    return HttpResponseBadRequest("You don't have permission to log in as a guest.")
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