"""
URL configuration for faciltyapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from register import views as v
from django.contrib.auth.views import LogoutView
from host.views import create_client, delete_client, send_message
# from host.views import user_list
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('guest/', include('Guest.urls')),
    path('', include('home.urls')),
    path('host/', include('host.urls')),
    path('register/', v.register, name='register'),
    path('login/', v.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_client/', create_client, name='create_client'),
    path('delete_client/<int:id>/', delete_client, name='delete_client'),
    path('send_message/', send_message, name='send_message'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)