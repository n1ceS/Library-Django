from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Reader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            firstName = form.cleaned_data.get('firstName')
            lastName = form.cleaned_data.get('lastName')
            phoneNumber = form.cleaned_data.get('phoneNumber')
            password = form.cleaned_data.get('password')
            repeatedPassword = form.cleaned_data.get('repeatedPassword')
            print(len(phoneNumber))
            if password != repeatedPassword:
                messages.error(request, "Hasła nie są takie same!")
                return redirect('register')
            if len(phoneNumber) != 9:
                print("XDDDDD")
                messages.error(request, "Numer telefonu musi mieć dokładnie 9 znaków!")
                return redirect('register')
            if  User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                messages.error(request, "Użytkownik już istnieje!")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=firstName, last_name=lastName)
                user.groups.add(Group.objects.get(name='Reader'))
                reader = Reader.objects.create(user=user, telephoneNumber=phoneNumber)
                reader.save()
                return redirect('login')
    form = RegisterUserForm()
    return render(request, "authentication/register.html", {"form" : form})

def login(request):
    return render(request, "authentication/login.html")
