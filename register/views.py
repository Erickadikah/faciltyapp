from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse


# registration view for the host
@csrf_exempt
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user using the overridden save method in the form
            # Now you can access the user object
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            eircode = form.cleaned_data.get('eircode')
            country = form.cleaned_data.get('country')
            user.phone = phone
            user.address = address
            user.eircode = eircode
            user.country = country
            user.save()  # Save user with additional fields
            print(user)
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("/login/")  # Redirect to login page or any other page after registration
        else:
            # Display error messages if the form is invalid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

# this is the login view as a host
@csrf_exempt
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
    
    
@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES['uploadFile']:
        document_name = request.POST['documentName']
        document_type = request.POST['documentType']
        uploaded_file = request.FILES['uploadFile']

        # Save the uploaded document to the database
        uploaded_document = uploaded_file(
            user=request.user,  # Assign the current user
            document_name=document_name,
            document_type=document_type,
            upload_file=uploaded_file
        )
        uploaded_document.save()

        return HttpResponse('Document uploaded successfully!')
    return HttpResponse('Invalid request.')