#-*- encoding: utf-8 -*-

from django.contrib import auth
from django.shortcuts import render, redirect
from zhidewen.models import Tag


def index(request):
    tags = Tag.objects.filter(used_count__gt=0)
    return render(request, 'tags/index.html', {'tags': tags})


def questions(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    return render(request, 'tags/show.html', {'tag': tag})

