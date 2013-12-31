#-*- encoding: utf-8 -*-

from django import http
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from zhidewen.models import Question
from zhidewen.forms import QuestionForm


def render_list(request, questions):
    page = Paginator(questions, 3)
    cur_page = page.page(request.GET.get('page', 1))
    context = {
        'page': cur_page,
        'questions': cur_page.object_list
    }
    return render(request, 'questions/list.html', context)


def newest(request):
    return render_list(request, Question.existed.newest())


def hottest(request):
    return render_list(request, Question.existed.hottest())


def unanswered(request):
    return render_list(request, Question.existed.unanswered())


@login_required
def ask(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question.objects.create(request.user, **form.cleaned_data)
            return redirect(reverse('question', args=(question.id, )))
    return render(request, 'questions/ask.html', {'form': form})


def show(request, question_id):
    question = Question.existed.get(pk=question_id)
    question.view_count += 1
    question.save()
    return render(request, 'questions/show.html', {'question': question})


@login_required
def update(request, question_id):
    question = Question.existed.get(pk=question_id)
    if not request.user == question.created_by:
        return http.HttpResponse('403')

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question.update(request.user, **form.cleaned_data)
            return redirect(reverse('question', args=(question.id, )))

    tag_names = question.tags.values_list('name', flat=True)
    initial = model_to_dict(question)
    initial['tag_names'] = ' '.join(tag_names)
    form = QuestionForm(initial)
    return render(request, 'questions/edit.html', {'form': form, 'question': question})


@login_required
def delete(request, question_id):
    Question.existed.get(pk=question_id).soft_delete()
    return redirect(reverse('home'))
