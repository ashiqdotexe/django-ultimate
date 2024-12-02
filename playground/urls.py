from django.urls import path
from django.shortcuts import render
from . views import say_hello

urlpatterns = [
    path("hello/", say_hello)
]