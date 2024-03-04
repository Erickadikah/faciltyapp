from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally log in the user automatically after registration
            # username = form.cleaned_data.get("username")
            # password = form.cleaned_data.get("password1")
            # user = authenticate(username=username, password=password)
            # login(request, user)
            return redirect(reverse('admin:index'))  # Redirect to admin panel
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})
