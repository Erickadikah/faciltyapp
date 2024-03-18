from django.shortcuts import render
from host.models import Client
from host.views import Client
from .models import UploadedDocument
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse



# Create your views here.
# this is the client dashboard
@login_required
@csrf_exempt
def index(request):
    # Check if the client is authenticated
    if 'client_id' in request.session:
        # Retrieve the client ID from the session
        client_id = request.session['client_id']
        
        # Retrieve the client based on the client ID
        try:
            client = Client.objects.get(id=client_id)
            return render(request, 'guest.html', {'client': client, 'authenticated': True})
        except Client.DoesNotExist:
            return HttpResponse("Client not found")
    else:
        return HttpResponse("You must be as our client logged in to view this page.")


@csrf_exempt
def upload_document(request):
    if request.method == 'POST' and request.FILES['uploadFile']:
        document_name = request.POST['documentName']
        document_type = request.POST['documentType']
        uploaded_file = request.FILES['uploadFile']

        # Save the uploaded document to the database
        uploaded_document = UploadedDocument(
            user=request.user,  # Assign the current user
            document_name=document_name,
            document_type=document_type,
            upload_file=uploaded_file
        )
        uploaded_document.save()

        return HttpResponse('Document uploaded successfully!')
    return HttpResponse('Invalid request.')