from django.urls import path
from . import views
# from .views import create_user

urlpatterns = [
    path('', views.index, name='index'),
    # path('create_user/', create_user, name='create_user'),
]