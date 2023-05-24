from django.contrib import admin
from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.LogoutUser, name='logout'),
    path('edit_profile', views.UpdateUser.as_view(), name='edit_profile'),
    path('edit_password', views.PassChangeView.as_view(), name='edit_password'),
    path('edit_success', views.PassEditSuccess, name='edit_success'),
    path('history', views.HistoryView.as_view(), name='history'),
]