import json
import datetime
from django.shortcuts import render, redirect
from .models import User, Message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.http import JsonResponse
import random
import string
from django.contrib.auth.hashers import make_password

from django.core.mail import send_mail

load_dotenv()

# Database setup
engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
Session = sessionmaker(bind=engine)

def index(request):
    users = User.objects.all()
    return render(request, "host.html", {'users': users})

@csrf_exempt
def create_client(request):
    if request.method == 'POST':
        try:
            # Retrieve form data from request.POST
            userName = request.POST.get('username')
            email = request.POST.get('email')
            phoneNumber = request.POST.get('phoneNumber')
            rentPayDate = request.POST.get('rentPayDate')
            rentEndDate = request.POST.get('rentEndDate')

            # Generate a temporary password
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            # Create user
            user = User.objects.create_user(
                username=userName,
                email=email,
                password=temp_password  # Set a temporary password
            )

            # Additional user attributes
            user.phone_number = phoneNumber
            user.rent_pay_date = rentPayDate
            user.rent_end_date = rentEndDate
            user.save()

            # Send login credentials to the client's email
            send_login_credentials(email, userName, temp_password)

            return JsonResponse({'message': 'User created successfully. Login credentials sent to email.'}, status=201)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Date should be in YYYY-MM-DD format'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def send_login_credentials(email, username, password):
    # Send email with login credentials
    subject = 'Your Account Credentials'
    message = f'Hello {username},\n\nYour account has been created. Please use the following credentials to log in:\nUsername: {username}\nPassword: {password}\n\nUpon login, you will be prompted to change your password.\n\nThank you!'
    from_email = 'erickadikah2030@gmail.com'
    send_mail(subject, message, from_email, [email])
    

@csrf_exempt
def delete_client(request, id):
    if request.method == 'DELETE':
        try:
            # Get the user data before deleting
            user = User.objects.filter(id=id).first()

            if user:
                # Serialize the user data
                user_data = serializers.serialize('json', [user])

                # Delete user
                user.delete()

                return JsonResponse({'message': 'User deleted successfully', 'user': user_data}, status=200)
            else:
                return JsonResponse({'error': 'User with specified ID does not exist'}, status=404)

        except Exception as e:
            # Log the error
            print(e)
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def send_message(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        message_text = request.POST.get('message')
        pdf_file = request.FILES.get('pdf_file')  # Assuming the file input field name is 'pdf_file'

        try:
            # Retrieve the user based on the provided user ID
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Create a new message instance associated with the user and save it to the database
        message = Message(user=user, text=message_text)
        message.save()

        # Save the uploaded PDF file to the server
        if pdf_file:
            fs = FileSystemStorage()
            filename = fs.save(pdf_file.name, pdf_file)

            # You can associate the PDF file with the message or user if needed
            # For example:
            # message.attachment = filename
            # message.save()

        # You can perform additional actions here, such as sending notifications

        return JsonResponse({'success': True, 'message': 'Message sent successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)