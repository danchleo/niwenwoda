#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
import django_wysiwyg



class QuestionForm(forms.Form):

    title = forms.CharField(label=u'标题', max_length=300)
    content = forms.CharField(label=u'内容', widget=forms.Textarea, required=False)
    tag_names = forms.CharField(label=u'标签', max_length=300, required=False)

    def clean_tag_names(self):
        return self.cleaned_data['tag_names'].split(' ')

    def clean_content(self):
        return django_wysiwyg.sanitize_html(self.cleaned_data['content'])

    def clean(self):
        from lxml.html import html5parser
        cleaned_data = super(QuestionForm, self).clean()
        doc = html5parser.fromstring(cleaned_data['content'])
        cleaned_data['summary'] = doc.xpath("string()")[:500]
        return cleaned_data


class AnswerCreationForm(forms.Form):
    content = forms.CharField(label=u'回答', widget=forms.Textarea, required=True)

    def clean_content(self):
        return django_wysiwyg.sanitize_html(self.cleaned_data['content'])
