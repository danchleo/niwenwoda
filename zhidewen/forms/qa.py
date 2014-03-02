#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class QuestionForm(forms.Form):

    title = forms.CharField(label=u'标题', max_length=300)
    content = forms.CharField(label=u'内容', widget=forms.Textarea, required=False)
    tag_names = forms.CharField(label=u'标签', max_length=300, required=False)

    def clean_tag_names(self):
        return self.cleaned_data['tag_names'].split(' ')


class AnswerCreationForm(forms.Form):
    content = forms.CharField(label=u'回答', widget=forms.Textarea, required=True)
