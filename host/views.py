from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ClientForm, GuestLoginForm
from .models import Client
from django.http import JsonResponse
from django.contrib.auth.models import User
import random
import string
from django.contrib.auth.models import User, Permission
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


CustomUser = get_user_model()

def index(request):
    clients = Client.objects.filter(user=request.user)
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
            client.creator_id = request.user.id
            client.save()

            # Create user and assign permission
            password = generate_random_password()
            user = User.objects.create_user(username=client.email, password=password)
            user.user_permissions.add(Permission.objects.get(codename='can_login_as_guest'))
            print("clint username", client.username)
            print("Client after saving:", client.email)
            print("Client after saving:", client.phoneNumber)
            print("Client after saving:", client.rentPayDate)
            print("Client after saving:", client.rentEndDate)
            print("creatorid", client.creator_id)
            print("pass", password)

            # Set the password directly on the User object
            user.set_password(password)
            # password.save()
            user.save()

            # Refresh clients after saving new client
            clients = Client.objects.all()

            print('Generated password:', password)

        return render(request, 'host.html', {'clients': clients})
    else:
        form = ClientForm()
    
    return render(request, 'host.html', {'clients': clients, 'form': form})

@csrf_exempt
def guest_login(request):
    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        
        # Print the user before processing the form submission
        print("User before form submission:", request.user)
    
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Corrected to 'email'
            print("Email:", email)
            password = form.cleaned_data.get('password')
            print("Password:", password)
            user = authenticate(request, username=email, password=password)  # Passing 'email' as username
            if user:
                print("User after authentication:", user)
                print("User has permission to log in as guest:", user.has_perm('accounts.can_login_as_guest'))
                # Log in the user
                login(request, user)
                return redirect('/guest/')
            else:
                # Handle invalid credentials
                return JsonResponse({'success': False, 'message': 'Invalid email or password'})
        else:
            # Handle form validation errors
            if 'email' in form.errors:
                error_message = 'Email is required.'
            elif 'password' in form.errors:
                error_message = 'Password is required.'
            else:
                error_message = 'Invalid email or password.'
            
            return JsonResponse({'success': False, 'message': error_message})
    else:
        # Handle GET request by rendering the login form
        form = GuestLoginForm()
        return render(request, 'guest_login.html', {'form': form})




# display all clients
def display_clients(request):
    clients = Client.objects.all()
    return render(request, 'host.html', {'clients': clients})

def display_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients})
@csrf_exempt
def delete_client(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect('create_client')

#get client with id
# @login_required
def get_client(request, user_id, client_id):
    if request.method == 'GET':
        try:
            # Retrieve the client with the specified ID associated with the specified user
            client = get_object_or_404(Client, id=client_id, user_id=user_id)
            # Return client data in JSON format
            return JsonResponse({'id': client.id, 'username': client.username, 'email': client.email, 'phoneNumber': client.phoneNumber, 'rentPayDate': client.rentPayDate, 'rentEndDate': client.rentEndDate, 'creator_id': client.creator_id, 'user_id': client.user_id})
        except Client.DoesNotExist:
            # Return an error response if the client is not found or not associated with the user
            return JsonResponse({'error': 'Client not found'}, status=404)
        
#user
def get_user(request, user_id):
    if request.method == 'GET':
        try:
            # Retrieve the user with the specified ID
            user = get_object_or_404(User, id=user_id)
            # Retrieve all clients associated with the user
            clients = Client.objects.filter(user=user)
            # Return user and client data in JSON format
            user_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'clients': [{'id': client.id, 'username': client.username, 'email': client.email} for client in clients]
                }
            return JsonResponse(user_data)
        except User.DoesNotExist:
            # Return an error response if the user is not found
            return JsonResponse({'error': 'User not found'}, status=404)
        
# dispaly all users
def display_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                }
            user_list.append(user_data)
        return JsonResponse(user_list, safe=False)
    
def get_all_clients(request):
    if request.method == 'GET':
        # Retrieve all clients from the database
        clients = Client.objects.all()
        
        # Serialize client data into JSON format
        client_data = [{'id': client.id, 'username': client.username, 'email': client.email} for client in clients]
        
        # Return the serialized client data as JSON response
        return JsonResponse({'clients': client_data})