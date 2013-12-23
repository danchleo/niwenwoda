#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class QuestionForm(forms.Form):

    title = forms.CharField(label=u'标题', max_length=300)
    content = forms.CharField(label=u'内容', widget=forms.Textarea, required=False)
    tag_names = forms.CharField(label=u'标签', max_length=300, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['tag_names'] = cleaned_data['tag_names'].split(' ')
        return cleaned_data


class AnswerCreationForm(forms.Form):
    content = forms.CharField(label=u'回答', widget=forms.Textarea, required=True)
