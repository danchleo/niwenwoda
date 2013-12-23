#-*- encoding: utf-8 -*-


from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect, render_to_response
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from zhidewen.models import Tag


def index(request):
    """
    标签墙页面
    """
    tags = Tag.objects.filter(used_count__gt=0)
    return render(request, 'tags/index.html', {'tags': tags})


def questions(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    return render(request, 'tags/show.html', {'tag': tag})


def hotest(request):
    """
    返回一个热门标签列表
    """
    tags = Tag.existed.order_by('-used_count').all()[0:10]
    hostest_tags_info = {}
    for tag in tags:
        hostest_tags_info[tag.id] = {
            'name': tag.name,
            'used_count': tag.used_count,
            'url': reverse('tag', kwargs={'tag_name': tag.name})
        }
    return HttpResponse(json.dumps(hostest_tags_info))