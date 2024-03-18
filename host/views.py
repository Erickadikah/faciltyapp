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
import logging
from django.contrib.auth.hashers import make_password
from .permisions import remove_duplicate_permissions

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
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.creator_id = request.user.id
            client.save()

            # Generate a random password
            password = generate_random_password()
            
            # Check if a user with the same email already exists
            user_exists = User.objects.filter(username=client.email).exists()
            if not user_exists:
                # Create a new User object
                user = User.objects.create(username=client.email)
                
                # Assign the 'can_login_as_guest' permission to the user if not already assigned
                try:
                    permission = Permission.objects.get(codename='can_login_as_guest')
                except Permission.DoesNotExist:
                    # Create the permission if it doesn't exist
                    permission = Permission.objects.create(codename='can_login_as_guest', name='Can log in as guest')

                # Check if the permission is not already assigned to the user
                if not user.has_perm('accounts.can_login_as_guest'):
                    user.user_permissions.add(permission)
            else:
                # Return a JSON response indicating that the email already exists
                return JsonResponse({'success': False, 'message': 'User with this email already exists'})
                
            # Set the password and save the user
            user.set_password(password)
            user.save()
                
            # Log the details
            print("Client username:", client.username)
            print("Client email:", client.email)
            print("Client phone number:", client.phoneNumber)
            print("Client rent pay date:", client.rentPayDate)
            print("Client rent end date:", client.rentEndDate)
            print("Creator ID:", client.creator_id)
            print("Generated password:", password)
                
            # Return a success response
            return JsonResponse({'success': True, 'message': 'Client created successfully', 'password': password})
            
        else:
            # Return a JSON response with form errors
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': form.errors})
    else:
        # Return a JSON response for invalid request method
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
logger = logging.getLogger(__name__)

@csrf_exempt
@csrf_exempt
def guest_login(request):
    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        
        # Check if the form data is valid
        if form.is_valid():
            # Extract email and password from the form
            email = form.cleaned_data.get('email')
            print(email)
            password = form.cleaned_data.get('password')
            print("email")
            # print("user:", User.objects.get(username=email)
            print(password)
            
            # Authenticate the user
            user = authenticate(request, username=email, password=password)
            
            # Check if authentication is successful
            if user:
                # Check if the user has the required permission
                # if user.has_perm('can_login_as_guest'):
                    # Log in the user
                    login(request, user)
                    return redirect('/guest/')
                # else:
                    # User does not have the required permission
                    return JsonResponse({'success': False, 'message': 'User does not have permission to login as guest'})
            else:
                # Invalid email or password
                return JsonResponse({'success': False, 'message': 'Invalid email or password'})
        else:
            # Form validation failed
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': form.errors})
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
                # 'phone': user.phone,
                # 'address': user.address,
                # 'aircode': user.eircode,
                # 'country': user.country,
                'client_count': clients.count(),
                'clients': [{'id': client.id, 'username': client.username, 'email': client.email,} for client in clients]
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