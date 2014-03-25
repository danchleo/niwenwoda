#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
import html5lib
from html5lib import sanitizer, treebuilders, treewalkers, serializer

# from django-wysiwyg
def sanitize_html(input):
    """
    Removes any unwanted HTML tags and attributes, using html5lib.

    >>> sanitize_html5lib("foobar<p>adf<i></p>abc</i>")
    u'foobar<p>adf<i></i></p><i>abc</i>'
    >>> sanitize_html5lib('foobar<p style="color:red; remove:me; background-image: url(http://example.com/test.php?query_string=bad);">adf<script>alert("Uhoh!")</script><i></p>abc</i>')
    u'foobar<p style="color: red;">adf&lt;script&gt;alert("Uhoh!")&lt;/script&gt;<i></i></p><i>abc</i>'
    """

    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer, tree=treebuilders.getTreeBuilder("dom"))
    dom_tree = p.parseFragment(input)
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)

    s = serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False)
    return "".join(s.serialize(stream))


def plain_text(html):
    return "".join(html5lib.parse(html).itertext())


class QuestionForm(forms.Form):

    title = forms.CharField(label=u'标题', max_length=300)
    content = forms.CharField(label=u'内容', widget=forms.Textarea, required=False)
    tag_names = forms.CharField(label=u'标签', max_length=300, required=False)

    def clean_tag_names(self):
        return self.cleaned_data['tag_names'].split(' ')

    def clean_content(self):
        return sanitize_html(self.cleaned_data['content'])

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        cleaned_data['summary'] = plain_text(cleaned_data['content'])[:500]
        return cleaned_data


class AnswerCreationForm(forms.Form):
    content = forms.CharField(label=u'回答', widget=forms.Textarea, required=True)

    def clean_content(self):
        return sanitize_html(self.cleaned_data['content'])
