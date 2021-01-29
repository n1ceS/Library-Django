from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Reader, Book, Hirement
from django.utils import timezone
from django.contrib.auth.models import User, Group
from .forms import RegisterUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
# Create your views here.
import random

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

@unauthenticated_user
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
    return render(request, "authentication/register.html", {"form" : form })

@unauthenticated_user
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_superuser:
                    return  redirect('/admin')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, "Niepoprawne dane logowania!")
                return redirect('login')
    form = LoginForm()
    return render(request, "authentication/login.html", {"form" : form })

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/login')
def get_all_books(request):
    books = Book.objects.all()
    return render(request, 'books.html', { 'books' : books})

@login_required(login_url='/login')
def reservation(request,pk):
    if(request.method == 'POST'):
        answer = request.POST['days']
        if answer == '0':
            messages.error(request, "Nie wybrano liczby dni!")
            return redirect('reserve', pk)
        else:
            qrcode = random.getrandbits(128)
            hire_date = timezone.now()
            expiration_date = timezone.now() + timezone.timedelta(days=int(answer))
            book = Book.objects.get(pk=pk)
            if(book is None):
                return redirect('dashboard')
            reader = Reader.objects.get(user=request.user)
            hirement = Hirement.objects.create(qrcode=qrcode, hire_date=hire_date, expiration_date=expiration_date, reader=reader, book=book)
            return render(request, 'hirementSuccess.html', {'hirement' : hirement})
    else:
        book = Book.objects.get(pk=pk)
        reader = Reader.objects.get(user=request.user)
        return render(request, 'reserve.html', {'book' : book, "reader" : reader })
