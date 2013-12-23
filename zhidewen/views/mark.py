#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def mark(request):
    """
    标记，相当于收藏
    通过 Ajax 方式发送 POST 请求
        content_type: 'question' / 'answer'
        object_pk: '...'
    """
    if request.method == 'POST':
        return HttpResponse('')
    return HttpResponse('')

@login_required
def unmark(request):
    """
    取消标记
    通过 Ajax 方式发送 POST 请求
        content_type: 'question' / 'answer'
        object_pk: '...'
    """
    if request.method == 'POST':
        return HttpResponse('')
    return HttpResponse('')

def marked(request, user_id):
    """
    获取用户的收藏列表
    通过 Ajax 方式发送 POST 请求
        content_type: 'question' / 'answer'
    """
    return HttpResponse('')