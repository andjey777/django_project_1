from django.contrib import admin
from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainView, name='home'),
    path('info', views.OutputInfo.as_view(), name='info'),
    path('ram', views.GetRam.as_view(), name='ram'),
    path('processor', views.GetProc.as_view(), name='processor'),
    path('grcard', views.GetGrCard.as_view(), name='grcard'),
    path('recommend', views.Recommend.as_view(), name='recom'),
    path('builder', views.BuilderView.as_view(), name='builder'),
    path('motherboard', views.GetMotherboard.as_view(), name='motherboard'),
]