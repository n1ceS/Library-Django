
from django import forms

class RegisterUserForm(forms.Form):
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
    phoneNumber = forms.RegexField(regex=r'^\+?1?\d{9,15}$',min_length=9, max_length=9,
        required=True,
        widget=forms.NumberInput(attrs={'class': "input"})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': "input"})
    )
    repeatedPassword = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': "input"})
    )
