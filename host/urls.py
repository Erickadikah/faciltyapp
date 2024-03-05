from django.urls import path
from .views import user_list
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_list/', user_list, name='user_list'),
]