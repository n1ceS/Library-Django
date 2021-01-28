from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterUserForm(response.POST)
        if form.is_valid():
            form.save()
    form = RegisterUserForm()
    return render(response, "register/register.html", {"form" : form})