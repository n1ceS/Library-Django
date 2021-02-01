
from django import forms

class RegisterUserForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class' : "input"})
    )
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={'class' : "input"})
    )
    firstName = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': "input"})
    )
    lastName = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': "input"})
    )
    phoneNumber = forms.CharField(required=True,
        widget=forms.NumberInput(attrs={'class': "input"}))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': "input"})
    )
    repeatedPassword = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': "input"})
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class' : "input"})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': "input"})
    )

class ContactForm(forms.Form):
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'subject-input'}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'class' : 'message-input', 'rows' : "10", 'cols':"70"}))