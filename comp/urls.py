from django.contrib import admin
from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', views.MainView, name='home'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.LogoutUser, name='logout'),
    path('info', views.OutputInfo, name='info'),
    path('ram', views.GetRam, name='ram'),
    path('processor', views.GetProc, name='processor'),
    path('grcard', views.GetGrCard, name='grcard'),
    path('recommend', views.Recommend, name='recom'),
    path('edit_profile', views.UpdateUser.as_view(), name='edit_profile'),
    path('edit_password', views.PassChangeView.as_view(), name='edit_password'),
    path('edit_success', views.PassEditSuccess, name='edit_success'),
    path('history', views.HistoryView, name='history'),
    path('builder', views.BuilderView, name='builder'),
    path('motherboard', views.GetMotherboard, name='motherboard'),
]