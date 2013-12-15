#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from zhidewen.models.question import Question


class Answer(models.Model):
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
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name=u'最后更新时间')
    deleted = models.BooleanField(default=False, verbose_name=u'是否被删除')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_answers'
