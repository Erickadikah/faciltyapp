from django.urls import path
from . import views
# from .views import client_created
from .views import create_client, display_clients

urlpatterns = [
    path('', views.index, name='index'),
    path('create_client/', create_client, name='create_client'),
    path('display_clients/', display_clients, name='display_clients'),

]
