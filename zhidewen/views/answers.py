#-*- encoding: utf-8 -*-

from django import http
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from zhidewen.models import Question, Answer
import json


@login_required
def answer_question(request, question_id):
    question = Question.existed.get(pk=question_id)
    content = request.POST.get('content')
    if not content:
        return http.HttpResponse('required content')
    answer = Answer.objects.answer_question(request.user, question, content)
    if request.is_ajax():
        return http.HttpResponse(json.dumps(model_to_dict(answer)))
    else:
        return redirect(reverse('question', args=(question_id,)))


@login_required
def update(request, id):
    answer = Answer.existed.get(pk=id)
    content = request.POST.get('content')
    if request.method == 'POST' and content:
        answer.update(request.user, content=content)
        return redirect(reverse('question', args=(answer.question.id,)))
    return render(request, 'answers/edit.html', {'answer': answer})


@login_required
def delete(request, id):
    answer = Answer.existed.get(pk=id)
    answer.soft_delete()
    return redirect(reverse('question', args=(answer.question.id,)))
