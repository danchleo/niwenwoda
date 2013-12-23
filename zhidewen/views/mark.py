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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from zhidewen.models import Mark, Question, Answer


@login_required
def mark_question(request, question_id):
    """
    标记提问
    /q/[question_id]/vote
    """
    return _mark(request, Question.existed.get(pk=question_id))


@login_required
def mark_answer(request, answer_id):
    """
    标记答案
    /a/[answer_id]/vote
    """
    return _mark(request, Answer.existed.get(pk=answer_id))


def _mark(request, obj):
    value = request.GET.get('value')
    if not value in ('1', '0', '-1'):
        return HttpResponse('value error')
    Mark.objects.vote(request.user, obj, int(value))
    status = {'mark_count': obj.mark_count}
    return HttpResponse(json.dumps(status))


def marked(request, marked_type=None):
    """
    获取用户的收藏列表
    marked_type: 'question' / 'answer'
    """
    if marked_type not in ['question', 'answer']:
        marked_type = None
    user = request.user
    template_file = 'users/marked.html' if marked_type is None else 'users/marked_%ss.html' % marked_type
    return render(request, template_file, {})