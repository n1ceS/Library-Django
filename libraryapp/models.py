from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


def generate_expiration_date():
    return timezone.now() + timezone.timedelta(days=30)

class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephoneNumber = models.CharField(null=True, blank=True, max_length=9)

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return  self.category

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='libraryapp/static/uploads/books/', default='libraryapp/static/uploads/books/default.jpg')
    description = models.CharField(max_length=500, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.author)  + " " + self.title
class Hirement(models.Model):
    id = models.AutoField(primary_key=True)
    qrcode = models.CharField(max_length= 200, null=True, blank=True)
    hire_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    expiration_date = models.DateTimeField(null=True, blank=True, default=generate_expiration_date)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, null=True, on_delete=models.CASCADE, blank=True)
    status = models.CharField(max_length=30, default="Zarezerwowana")