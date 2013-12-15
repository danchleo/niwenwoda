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


class Answer(models.Model):
    objects = AnswerManager()
    exsited = AnswerManager.existed_manager()

    question = models.ForeignKey(Question, related_name='answers', verbose_name=u'问题')
    content = models.TextField(verbose_name=u'答案')

    up_count = models.PositiveIntegerField(default=0, verbose_name=u'赞成数')
    down_count = models.PositiveIntegerField(default=0, verbose_name=u'反对数')
    comment_count = models.PositiveIntegerField(default=0, verbose_name=u'评论数')
    mark_count = models.PositiveIntegerField(default=0, verbose_name=u'标记数')
    ranking_weight = models.IntegerField(default=0, verbose_name=u'权重')

    created_by = models.ForeignKey(User, related_name='answers', verbose_name=u'创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    last_updated_by = models.ForeignKey(User, verbose_name=u'最后更新人')
    last_updated_at = models.DateTimeField(auto_now_add=True, verbose_name=u'最后更新时间')

    deleted = models.BooleanField(default=False, verbose_name=u'是否被删除')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_answers'

    def save(self, *args, **kwargs):
        self.ranking_weight = self.count_ranking()
        return super(Answer, self).save(*args, **kwargs)

    def count_ranking(self):
        return self.up_count - self.down_count

    def soft_delete(self):
        self.deleted = True
        return self.save()

    def update(self, user, content):
        self.content = content
        self.last_updated_by = user
        self.last_updated_at = timezone.now()
        return self.save()

    def __repr__(self):
        return '<Answer: %s>' % self.id
