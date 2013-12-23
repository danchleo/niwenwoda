#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class TagForm(forms.Form):
    name = forms.CharField(label=u'名称', max_length=30)
    description = forms.CharField(label=u'描述', widget=forms.Textarea, required=False)
    icon = forms.URLField(label=u'图标', required=False)
