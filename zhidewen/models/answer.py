#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from zhidewen.models import base
from zhidewen.models.question import Question
from django.utils import timezone


class AnswerQuerySet(base.QuerySet):

    def best(self):
        return self.order_by('-ranking_weight')

    def oldest(self):
        return self.order_by('created_at')


class AnswerManager(AnswerQuerySet.as_manager()):

    def answer_question(self, user, question, content, **kwargs):
        return self.create(content=content, question=question, created_by=user, last_updated_by=user, **kwargs)


class Answer(base.ContentModel):
    objects = AnswerManager()
    exsited = AnswerManager.existed_manager()

    question = models.ForeignKey(Question, related_name='answers', verbose_name=u'问题')
    content = models.TextField(verbose_name=u'答案')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_answers'

    def count_ranking(self):
        return self.up_count - self.down_count
