from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from .models import User
# from .forms import UserForm

# Create your views here.

def index(request):
    users = User.objects.all()
    return render(request, "host.html", {'users': users})

# user creation view
# def create_user(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success')  # Redirect to a success page
#     else:
#         form = UserForm()
#     return render(request, 'create_user.html', {'form': form})