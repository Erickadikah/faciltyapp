from django.urls import path
# from .views import user_profile

from . import views

urlpatterns = [
    path('', views.index, name='index'),

]