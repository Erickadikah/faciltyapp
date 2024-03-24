from django.shortcuts import render
from host.models import Client
from host.views import Client
from .models import UploadedDocument
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from .forms import DocumentUploadForm
from django.http import JsonResponse
from django.contrib.auth.models import User



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

# @login_required
@csrf_exempt
def upload_document(request, client_id):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            client = Client.objects.get(id=client_id)
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']
            
            # Get the creator of the client
            creator_id = client.creator_id
            print("creator:", creator_id)
            
            try:
                recipient_user = User.objects.get(id=creator_id)
                print("recipient:", recipient_user)
            except User.DoesNotExist:
                return JsonResponse({"error": "User who created the client not found"}, status=404)
            
            uploaded_document = UploadedDocument(
                sender=client,
                recipient_user=recipient_user,
                description=description,
                file=file
            )
            uploaded_document.save()
            print("the doc:", uploaded_document)
            
            return JsonResponse({"success": "Document uploaded successfully!"})
        else:
            errors = form.errors.as_json()
            return JsonResponse({"error": "Form validation failed", "errors": errors}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
# @login_required
#gett all documents
# @csrf_exempt
# def get_documents(request, client_id):
#     if request.method == 'GET':
#         client = Client.objects.get(id=client_id)
#         documents = UploadedDocument.objects.filter(sender=client)
#         document_list = []
#         for document in documents:
#             document_data = {
#                 'id': document.id,
#                 'description': document.description,
#                 'file': document.file.url
#             }
#             document_list.append(document_data)
#         return JsonResponse(document_list, safe=False)
#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=405)




# import boto3
# from django.conf import settings

# def upload_document(request, client_id):
#     if request.method == 'POST':
#         form = DocumentUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             client = Client.objects.get(id=client_id)
#             description = form.cleaned_data['description']
#             file = form.cleaned_data['file']
            
#             # Get the creator of the client
#             creator_id = client.creator_id
            
#             try:
#                 recipient_user = User.objects.get(id=creator_id)
#             except User.DoesNotExist:
#                 return JsonResponse({"error": "User who created the client not found"}, status=404)
            
#             # Save file to S3
#             s3 = boto3.client('s3',
#                               aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
#             bucket_name = settings.AWS_STORAGE_BUCKET_NAME
#             s3.upload_fileobj(file, bucket_name, file.name)
#             file_url = f"https://{bucket_name}.s3.amazonaws.com/{file.name}"
            
#             # Create UploadedDocument instance
#             uploaded_document = UploadedDocument(
#                 sender=client,
#                 recipient_user=recipient_user,
#                 description=description,
#                 file=file_url  # Save S3 URL instead of file object
#             )
#             uploaded_document.save()
            
#             return JsonResponse({"success": "Document uploaded successfully!"})
#         else:
#             errors = form.errors.as_json()
#             return JsonResponse({"error": "Form validation failed", "errors": errors}, status=400)
#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=405)