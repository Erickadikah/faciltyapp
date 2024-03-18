from django.shortcuts import render
from host.models import Client
from host.views import Client
from .models import UploadedDocument
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        client = Client.objects.filter(user=request.user.id).first()
        print(client)
        return render(request, 'guest.html', {'client': client})
    else:
        return HttpResponse("You must be logged in to view this page.")

# def index(request):
#     return render(request, 'guest.html', )

def dashboard(request):
    client = Client.objects.get(user=request.user)

    context = {
        'user': request.user,
        'client': client  # Pass the client object to the template context
    }

    return render(request, 'guest.html', context)
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