#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect, render_to_response
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from zhidewen.models import Question, Answer
import json


@login_required
def answer_question(request, question_id):
    question = Question.existed.get(pk=question_id)
    content = request.POST.get('content')
    if not content:
        return HttpResponse('required content')
    answer = Answer.objects.answer_question(request.user, question, content)
    if request.is_ajax():
        return HttpResponse(json.dumps(model_to_dict(answer)))
    else:
        return redirect(reverse('question', args=(question_id,)))


@login_required
def update(request, answer_id):
    answer = Answer.existed.get(pk=answer_id)
    content = request.POST.get('content')
    if request.method == 'POST' and content:
        answer.update(request.user, content=content)
        return redirect(reverse('question', args=(answer.question.id,)))
    return render(request, 'answers/edit.html', {'answer': answer})


@login_required
def delete(request, answer_id):
    answer = Answer.existed.get(pk=answer_id)
    answer.soft_delete()
    return redirect(reverse('question', args=(answer.question.id,)))

@login_required
def close(request, answer_id):
    answer = Answer.existed.get(pk=answer_id)
    answer.close()
    return HttpResponse(json.dumps({
        'status': 'success' if answer.close else 'failure'
    }))
