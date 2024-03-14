from django.shortcuts import render
from host.models import Client

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        client = Client.objects.filter(user=request.user).first()
        return render(request, 'guest.html', {'client': client})
    else:
        return HttpResponse("You must be logged in to view this page.")
    

# def user_profile(request):
#     return render(request, "user_profile.html")