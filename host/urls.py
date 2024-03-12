from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Example URL pattern
    # Add more URL patterns for other views as needed
]
