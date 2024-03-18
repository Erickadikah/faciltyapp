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
from django.contrib.auth.hashers import check_password

CustomUser = get_user_model()

def index(request):
    clients = Client.objects.filter(creator_id=request.user.id)
    return render(request, "host.html", {'clients': clients})

def generate_random_password():
    # Generate a random password of length 8
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# this is how the host create a client or guest
@csrf_exempt
@login_required
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.creator_id = request.user.id  # or however you want to track the creator
            client.save()  # Make sure to save the client instance to trigger the save() method
            
            # Ensure that the password is generated and saved after the client object is saved
            client.password = client.generate_random_password()  # Generate a random password
            print("Password:", client.password)  # Make sure the password is populated before saving
            client.save()  # Save the client object again to update the password field
            
            # Log the details (optional)
            print("Client username:", client.username)
            print("Client email:", client.email)
            print("Client phone number:", client.phoneNumber)
            print("Client rent pay date:", client.rentPayDate)
            print("Client rent end date:", client.rentEndDate)
            print("Creator ID:", client.creator_id)
            print("Password:", client.password)  # Make sure the password is populated after saving
            
            # Return a success response
            return JsonResponse({'success': True, 'message': 'Client created successfully'})
        else:
            # Return a JSON response with form errors
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': form.errors})
    else:
        # Return a JSON response for invalid request method
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
 
logger = logging.getLogger(__name__)

#this is the login view as a guest
@csrf_exempt
def guest_login(request):
    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print("email:", email)
            password = form.cleaned_data.get('password')
            print("password:", password)

            # Authenticate the guest user
            client = Client.objects.filter(email=email).first()
            print("client:", client)

            if client is not None:
                if check_password(password, client.password):
                    # Log in the guest client
                    request.session['client_id'] = client.id
                    return redirect('/guest/')  # Redirect to guest area
                else:
                    # Incorrect password
                    print("Incorrect password for client:", client.username)
                    return JsonResponse({'success': False, 'message': 'Invalid email or password'})
            else:
                # Client not found
                print("Client with email {} not found.".format(email))
                return JsonResponse({'success': False, 'message': 'Client not found'})
        else:
            # Form validation failed
            print("Form validation failed:", form.errors)
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': form.errors})
    else:
        # Render the guest login form
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