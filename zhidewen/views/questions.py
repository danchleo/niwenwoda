#-*- encoding: utf-8 -*-

from django import forms
from django import http
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from zhidewen.models import Question


class QuestionForm(forms.Form):

    title = forms.CharField(label=u'标题')
    content = forms.CharField(label=u'内容')
    tag_names = forms.CharField(label=u'标签')

    def clean(self):
        cd = self.cleaned_data
        cd['tag_names'] = cd['tag_names'].split(' ')
        return cd


def render_list(request, questions):
    context = {
        'questions': questions,
        'answered_count': questions.answered().count(),
        'unanswered_count': questions.unanswered().count(),
    }
    return render(request, 'questions/index.html', context)


def newest(request):
    return render_list(request, Question.existed.fresh())


def hottest(request):
    return render_list(request, Question.existed.hot())


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
    return render(request, 'questions/new.html', {'form': form})


def show(request, id):
    question = Question.existed.get(pk=id)
    question.view_count += 1
    question.save()
    return render(request, 'questions/show.html', {'question': question})


@login_required
def update(request, id):
    question = Question.existed.get(pk=id)
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
def delete(request, id):
    Question.existed.get(pk=id).soft_delete()
    return redirect(reverse('home'))

