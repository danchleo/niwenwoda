#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import *
from zhidewen.models import User
from zhidewen.forms import RegisterForm, ProfileForm


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 验证
            user = authenticate(username=username, password=password)
            if user:
                django_login(request, user)
                # 如果用戶是在訪問某頁面的時候跳轉過來的，登陸成功之後自動轉向之
                # 前訪問的頁面。
                next_url = request.GET.get('next', reverse('index'))
                return HttpResponseRedirect(next_url)
            error(request, u'抱歉，不能通过验证！')
    else:
        form = AuthenticationForm()

    content = {
        'form': form,
        'title': u'登录',
    }

    return render_to_response('users/login.html', content,
                              context_instance=RequestContext(request))


@login_required
def logout(request):
    """
    退出，转向登录页面
    """
    django_logout(request)
    return HttpResponseRedirect(reverse('login'))


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    content = {
        'form': form,
        'title': u'注册',
    }

    return render_to_response('accounts/register.html', content,
                              context_instance=RequestContext(request))


def wall(request):
    """
    用户墙页面
    """
    users = User.objects.filter(is_active=True).order_by('-profile__reputation')
    context = {'users': users}
    return render_to_response('users/index.html', context,
                              context_instance=RequestContext(request))


def page(request, username):
    """
    用户主页
    eg: /u/catroll
    """
    user = User.objects.get(username=username)
    return render(request, 'users/show.html', {'user': user})


@login_required
def change_profile(request):
    """
    修改个人信息
    """
    if request.method == 'POST':
        pass
    else:
        form = ProfileForm()

    context = {
        'form': form
    }

    return render_to_response('users/index.html', context,
                              context_instance=RequestContext(request))


@login_required
def change_password(request):
    """
    修改密码
    """
    return HttpResponse('')


def most_prestigious(request):
    """
    返回 15 个最有声望的用户
    json api，给页面调用，可能用不上，暂时不管
    """
    users = User.objects.filter(is_active=True).order_by('-profile__reputation')[:10]
    print users
    return HttpResponse(json.dumps({}))


def contents(request, username, template):
    user = User.objects.get(username=username)
    return render(request, template, {'user': user})
