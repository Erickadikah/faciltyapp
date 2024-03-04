from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # This maps the root URL to the index view
    path('register/', views.register, name='register'),  # Add this line to map /register URL to the register view
]
