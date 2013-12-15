#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from zhidewen.models.tag import Tag


class Question(models.Model):
    title = models.CharField(max_length=140, verbose_name=u'标题')
    content = models.TextField(verbose_name=u'补充说明', null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=u'标签')
    view_count = models.PositiveIntegerField(default=0, verbose_name=u'浏览数')
    answer_count = models.PositiveIntegerField(default=0, verbose_name=u'回答数')
    up_count = models.PositiveIntegerField(default=0, verbose_name=u'赞成数')
    down_count = models.PositiveIntegerField(default=0, verbose_name=u'反对数')
    comment_count = models.PositiveIntegerField(default=0, verbose_name=u'评论数')
    mark_count = models.PositiveIntegerField(default=0, verbose_name=u'标记数')
    ranking_weight = models.IntegerField(default=0, verbose_name=u'权重')
    created_by = models.ForeignKey(User, related_name='questions', verbose_name=u'创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    last_updated_by = models.ForeignKey(User, verbose_name=u'最后更新人')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name=u'最后更新时间')
    last_refreshed_at = models.DateTimeField(auto_now=True, verbose_name=u'最后活跃时间')
    closed = models.BooleanField(default=False, verbose_name=u'是否被关闭')
    deleted = models.BooleanField(default=False, verbose_name=u'是否被删除')

    class Meta:
        db_table = 'zhidewen_questions'
