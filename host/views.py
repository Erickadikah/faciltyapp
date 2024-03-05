from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    return render(request, "host.html")

def user_list(request):
    users = User.objects.all()
    return render(request, "host/user_list.html", {"users": users})

def host(request):
    users = User.objects.all()
    return render(request, 'host.html', {'users': users})