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
# from .forms import MessageForm
from django.contrib import messages
from .models import Message
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password
from Guest.models import UploadedDocument


CustomUser = get_user_model()
@login_required
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
            client.creator_id = request.user.id

            # Generate a random password
            raw_password = generate_random_password()
            print("password:", raw_password)

            # Hash the raw password and save
            client.password = make_password(raw_password)
            # client.password.save()
            # print("saved:", password)

            # Save the client instance to trigger the save() method
            client.save()

            # Log the details
            logger.info("Client created: username=%s, email=%s, phoneNumber=%s, rentPayDate=%s, rentEndDate=%s, creator_id=%s",
                        client.username, client.email, client.phoneNumber, client.rentPayDate, client.rentEndDate, client.creator_id)

            return JsonResponse({'success': True, 'message': 'Client created successfully', 'password': raw_password})
        else:
            # Return a JSON response with form errors
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': form.errors})
    else:
        # Return a JSON response for invalid request method
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
logger = logging.getLogger(__name__)

#update client
@csrf_exempt
def update_client(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, id=client_id)  # Corrected 'id' to 'client_id'
        form = ClientForm(request.POST, instance=client)
        print("Password:", client.password)
        if form.is_valid():
            client = form.save(commit=False)
            client.creator_id = request.user.id  # or however you want to track the creator
            client.save()  # Make sure to save the client instance to trigger the save() method
            return JsonResponse({'success': True, 'message': 'Client updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Form validation failed', 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

#this is the login view as a guest
@csrf_exempt
def guest_login(request):
    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            password = form.cleaned_data.get('password')
            print(password)

            # Authenticate the guest user
            client = Client.objects.filter(email=email).first()
            print("client:", client)

            if client is not None:
                if check_password(password, client.password):
                    # Log in the guest client
                    request.session['client_id'] = client.id
                    logger.info("Guest login successful: email=%s", email)
                    return redirect('/guest/')  # Redirect to guest area
                else:
                    # Incorrect password
                    logger.error("Incorrect password for client: %s", client.username)
                    return JsonResponse({'success': False, 'message': 'Invalid email or password'})
            else:
                # Client not found
                logger.error("Client with email %s not found.", email)
                return JsonResponse({'success': False, 'message': 'Client not found'})
        else:
            # Form validation failed
            logger.error("Form validation failed: %s", form.errors)
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
            # clients = Client.objects.filter(user=user)
            # Return user and client data in JSON format
            user_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                # 'phone': user.phone,
                # 'address': user.address,
                # 'aircode': user.eircode,
                # 'country': user.country,
                # 'client_count': clients.count(),
                # 'clients': [{'id': client.id, 'username': client.username, 'email': client.email,} for client in clients]
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
    
def maintenance_view(request):
    return render(request, 'maintenance.html')

#sendig message
@login_required
@csrf_exempt
def send_message(request, client_id):
    if request.method == 'POST':
        sender = request.user  # Fetch the logged-in user as the sender
        print("Sender:", sender)  # Check sender

        # Fetch the recipient user by ID
        try:
            recipient_user = User.objects.get(pk=client_id)
            recipient_client = None  # Initialize recipient_client as None
        except User.DoesNotExist:
            # If the recipient is not a User, it might be a Client
            try:
                recipient_client = Client.objects.get(pk=client_id)
                recipient_user = None  # Initialize recipient_user as None
            except Client.DoesNotExist:
                print("Recipient does not exist")  # Print error message
                return JsonResponse({'error': 'Recipient does not exist'}, status=404)

        content = request.POST.get('message_text')
        file = request.FILES.get('file')

        # Create and save the message
        message = Message.objects.create(sender=sender, recipient_user=recipient_user, recipient_client=recipient_client, content=content, file=file)
        messages.success(request, 'Message sent successfully!')
        return JsonResponse({'success': True, 'message': 'Message sent successfully'})

    return render(request, 'send_message.html')

#maintainance view
def maintainance_view(request):
    return render(request, 'maintenance.html')


# get all messages from the database
def get_messages(request, client_id):
    if request.method == 'GET':
        # Retrieve all messages sent to the specified client
        messages = Message.objects.filter(recipient_client_id=client_id)
        
        # Serialize message data into JSON format
        message_data = [{'id': message.id, 'sender': message.sender.username, 'content': message.content, 'file': message.file.url if message.file else None, 'created_at': message.created_at} for message in messages]
        # print(message_data)
        # Return the serialized message data as JSON response
        return JsonResponse({'messages': message_data})

#delete messages
@require_POST
@csrf_exempt
def delete_message(request, message_id):
    try:
        # Check if the message exists
        message = Message.objects.get(pk=message_id)
        # Delete the message
        message.delete()
        return JsonResponse({'message': 'Message deleted successfully'}, status=200)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def get_documents(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            documents = UploadedDocument.objects.filter(recipient_user=user)
            document_list = []
            for document in documents:
                document_data = {
                    'sender': document.sender.username,
                    'id': document.id,
                    'description': document.description,
                    'file': document.file.url
                }
                document_list.append(document_data)
            return JsonResponse({'documents': document_list})  # Return an object with 'documents' property
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
#delet document with id
@require_POST
@csrf_exempt
def delete_document(request, document_id):
    try:
        document = UploadedDocument.objects.get(pk=document_id)
        document.delete()
        return JsonResponse({'message': 'Document deleted successfully'}, status=200)
    except UploadedDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)