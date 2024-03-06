from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    users = User.objects.all()
    return render(request, "host.html", {'users': users})

def user_list(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})

# def host(request):
#     users = User.objects.all()
#     return render(request, 'host.html', )