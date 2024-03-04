from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return HttpResponse("Guest Index Page")

def v1(response):
    return HttpResponse("view1 for guest index page")
