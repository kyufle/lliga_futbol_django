import django
from django.shortcuts import render
from django.urls import path

django.render = render

from . import views

urlpatterns = [
    path('classificacio/', views.classificacio, name='classificacio'),
]