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
