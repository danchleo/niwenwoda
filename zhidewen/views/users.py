#-*- encoding: utf-8 -*-

from django.shortcuts import render
from zhidewen.models import  User


def index(request):
    users = User.objects.all()
    return render(request, 'users/index.html', {'users': users})


def show(request, username):
    user = User.objects.get(username=username)
    return render(request, 'users/show.html', {'user': user})


def contents(request, username, template):
    user = User.objects.get(username=username)
    return render(request, template, {'user': user })