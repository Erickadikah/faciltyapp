from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return HttpResponse("Host Index Page")
# def index(request):
#     return render(request, 'host page')