from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password Again', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserUpdateForm(ModelForm):
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        required=False, label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ChangePassForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Repeat New Password',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
