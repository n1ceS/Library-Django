from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from .models import Reader, Book, Hirement, Author, Category, Message
from django.utils import timezone, translation
from django.contrib.auth.models import User, Group
from .forms import RegisterUserForm, LoginForm, ContactForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.db.models import F, Count
import itertools, json
# Create your views here.
import random,re
email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
telephone_regex = "^\\d{9}$"

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
    return render(request, "register.html", {"form" : form})

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
    return render(request, "login.html", {"form" : form})

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='/login')
def dashboard(request):
    cntx={}
    reader = Reader.objects.get(user = request.user)
    hire_books_count = Hirement.objects.filter(reader=reader).count()
    returned_books_count = Hirement.objects.filter(reader=reader, status="Zwrocona").count()
    to_return_books_count = hire_books_count - returned_books_count;

    cntx['hire_books_count'] = hire_books_count
    cntx['returned_books_count'] = returned_books_count
    cntx['to_return_books_count'] = to_return_books_count

    bestReaders = Reader.objects.annotate(books_count = Count('hirement')).order_by('-books_count')
    bestBooks = Book.objects.annotate(hire_count = Count('hirement')).order_by('-hire_count')
    cntx['top10users'] = itertools.islice(bestReaders, 10)
    cntx['top10books'] = itertools.islice(bestBooks, 10)
    return render(request, 'dashboard.html', {'info' : cntx})

@login_required(login_url='/login')
def get_all_books(request):
    empty = False
    books = Book.objects.all()
    if request.method == "POST" :
        selectedAuthor = request.POST['authors']
        selectedCategory = request.POST['categories']
        if selectedAuthor != "-1":
            books = books.filter(author=Author.objects.get(id=selectedAuthor))
        if selectedCategory != "-1":
            books = books.filter(category=Category.objects.get(id=selectedCategory))

    authors = Author.objects.all()
    categories = Category.objects.all()
    if not books:
        empty = True
    return render(request, 'books.html', { 'books' : books, 'authors' : authors, 'categories' : categories, 'empty' : empty})

@login_required(login_url='/login')
def reservation(request,pk):
    if(request.method == 'POST'):
        answer = request.POST['days']
        if answer == '0':
            messages.error(request, "Nie wybrano liczby dni!")
            return redirect('reserve', pk)
        else:
            qrcode = str(random.getrandbits(128))
            translation.activate('pl')
            hire_date = timezone.now()
            expiration_date = timezone.now() + timezone.timedelta(days=int(answer))
            book = Book.objects.get(pk=pk)
            if(book is None):
                return redirect('dashboard')
            if(book.count == 0):
                messages.error(request, "Aktualnie nie ma wolnego egzemplarza!")
                return redirect('reserve', pk)
            reader = Reader.objects.get(user=request.user)
            hirement = Hirement.objects.create(qrcode="R"+qrcode, hire_date=hire_date, expiration_date=expiration_date, reader=reader, book=book)
            Book.objects.filter(id=book.id).update(count=F('count')-1)
            sendEmail(hirement)
            return render(request, 'hirementSuccess.html', {'hirement' : hirement})
    else:
        book = Book.objects.get(pk=pk)
        reader = Reader.objects.get(user=request.user)
        return render(request, 'reserve.html', {'book' : book, "reader" : reader })

def sendEmail(hirement):
    html = get_template('emailTemplate.html')
    subject, from_email, to = "Potwierdzenie wypożyczenia " + hirement.book.title + " - QRLibrary", 'wypozyczenia@qrlibrary.com', hirement.reader.user.email
    html_content = html.render({'hirement': hirement})
    msg = EmailMultiAlternatives(subject, "", from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@login_required(login_url='/login')
def getHirements(request):
    translation.activate('pl')
    reader = Reader.objects.get(user = request.user)
    hirements = Hirement.objects.filter(reader = reader)
    return render(request, 'myhirements.html', {'hirements' : hirements})

@login_required(login_url='/login')
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            Message.objects.create(sender=request.user, subject=subject, message = message)
            messages.success(request, "Wiadomość została wysłana!")
            return redirect("contact")
    return render(request, 'contact.html', {'form' : form})

@login_required(login_url='/login')
def settings(request):
    reader = Reader.objects.get(user=request.user)
    if request.method == "POST" and request.POST.get('action') == "personal-password":
        password = request.POST.get('current-password')
        new_pasword = request.POST.get('new-password')
        if request.user.check_password(password):
            request.user.set_password(new_pasword)
            request.user.save()
            update_session_auth_hash(request, request.user)
            response = JsonResponse({"success": "Hasło zostało zmienione!"})
            response.status_code = 201
            return response
        else:
            response = JsonResponse({"error": "Nieprawidłowe hasło użytkownika!"})
            response.status_code = 401
            return response
    elif request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        telephone = request.POST['telephone']
        if username == "" or first_name == "" or last_name == "" or last_name == "" or email == "" or telephone == "":
            messages.error(request,"Wypełnij wszystkie pola!")
            return redirect("settings")
        if User.objects.get(username=username) is not None and username != request.user.username:
            messages.error(request, "Ktoś już ma taką nazwę użytkownika!")
            return redirect("settings")
        if not re.search(email_regex, email):
            messages.error(request, "Podaj poprawny adres email!")
            return redirect("settings")
        if User.objects.get(email=email) is not None and email != request.user.email:
            messages.error(request, "Konto z tym adresem email już istnieje!")
            return redirect("settings")
        if not re.search(telephone_regex, telephone):
            messages.error(request, "Podano niepoprawny numer telefonu!")
            return redirect("settings")
        Reader.objects.filter(user = reader.user).update(telephoneNumber=telephone)
        User.objects.filter(id=reader.user.id).update(username=username, first_name=first_name, last_name=last_name, email=email)
        reader = Reader.objects.get(user=request.user)
        messages.success(request, "Pomyślnie zaaktualizowano dane!")
    return render(request, 'settings.html', {'reader': reader})