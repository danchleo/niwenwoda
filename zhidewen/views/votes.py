#-*- encoding: utf-8 -*-

from django import http
from django.contrib.auth.decorators import login_required
from zhidewen.models import Vote, Question, Answer
import json


@login_required
def vote_question(request, id):
    return _vote(request, Question.existed.get(pk=id))


@login_required
def vote_answer(request, id):
    return _vote(request, Answer.existed.get(pk=id))


def _vote(request, obj):
    value = request.GET.get('value')
    if not value in ('1', '0', '-1'):
        return http.HttpResponse('value error')
    Vote.objects.vote(request.user, obj, int(value))
    status = {'up': obj.up_count, 'down': obj.down_count}
    return http.HttpResponse(json.dumps(status))

@login_required
def vote(request, obj_type, obj_pk, value):
    """
    投票
    /vote_up/question/1  => question, 1, 1
    /vote_down/answer/1  => answer, 1, -1 
    """
    return HttpResponse('')