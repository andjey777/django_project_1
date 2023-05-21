from django.contrib.auth.views import PasswordChangeView
from .models import RAM, Processor, GrapCard
from django.forms import ModelForm, TextInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class RAMForm(ModelForm):
    class Meta:
        model = RAM
        fields = ['name', 'capacity', 'frequency']
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RAM Name'
            }),
            "capacity": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RAM Capacity'
            }),
            "frequency": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ram Frequency'
            })
        }


class ProcForm(ModelForm):
    class Meta:
        model = Processor
        fields = ['name', 'cores', 'frequency']
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Processor Name'
            }),
            "cores": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Processor Cores'
            }),
            "frequency": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Processor Frequency'
            })
        }


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