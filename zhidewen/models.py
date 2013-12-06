#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='account', verbose_name=u'用户')
    nickname = models.CharField(max_length=100, verbose_name=u'昵称')
    birthday = models.DateField(verbose_name=u'出生日期')
    location = models.CharField(max_length=100, verbose_name=u'所在地')
    gender = models.CharField(max_length=10, verbose_name=u'性别')
    about = models.TextField(verbose_name=u'个人简介')
    website = models.URLField(verbose_name=u'个人网站')
    email_is_verified = models.BooleanField(verbose_name=u'邮箱地址是否已验证')

    class Meta:
        db_table = 'auth_user_profile'


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'名称')
    master = models.ForeignKey('self', related_name='slave_tags', verbose_name=u'主标签', null=True, blank=True)
    parent = models.ForeignKey('self', related_name='child_tags', verbose_name=u'父标签', null=True, blank=True)
    level = models.PositiveSmallIntegerField(verbose_name=u'层次', null=True, blank=True)
    icon = models.URLField(verbose_name=u'图标')
    description = models.TextField(verbose_name=u'描述')
    used_count = models.PositiveIntegerField(verbose_name=u'使用次数')
    created_by = models.ForeignKey(User, related_name='created_tags', verbose_name=u'创建人')
    created_at = models.DateTimeField(verbose_name=u'创建时间')
    deleted = models.BooleanField(verbose_name=u'是否被删除')

    class Meta:
        db_table = 'zhidewen_tags'


class Mark(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=u'', related_name='marks')
    object_pk = models.TextField()
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    marked_by = models.ForeignKey(User, related_name='marks', verbose_name=u'标记人')
    marked_at = models.DateTimeField(verbose_name=u'标记时间')

    class Meta:
        db_table = 'zhidewen_marks'


class Question(models.Model):
    title = models.CharField(max_length=140, verbose_name=u'标题')
    content = models.TextField(verbose_name=u'补充说明', null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=u'标签')
    view_count = models.PositiveIntegerField(verbose_name=u'浏览数')
    answer_count = models.PositiveIntegerField(verbose_name=u'回答数')
    up_count = models.PositiveIntegerField(verbose_name=u'赞成数')
    down_count = models.PositiveIntegerField(verbose_name=u'反对数')
    comment_count = models.PositiveIntegerField(verbose_name=u'评论数')
    mark_count = models.PositiveIntegerField(verbose_name=u'标记数')
    ranking_weight = models.IntegerField(verbose_name=u'权重')
    created_by = models.ForeignKey(User, related_name='questions', verbose_name=u'创建人')
    created_at = models.DateTimeField(verbose_name=u'创建时间')
    last_updated_by = models.ForeignKey(User, verbose_name=u'最后更新人')
    last_updated_at = models.DateTimeField(verbose_name=u'最后更新时间')
    closed = models.BooleanField(verbose_name=u'是否被关闭')
    deleted = models.BooleanField(verbose_name=u'是否被删除')

    class Meta:
        db_table = 'zhidewen_questions'
        ordering = ('created_at',)
        verbose_name = u'问题'
        verbose_name_plural = u'问题'


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name=u'问题')
    content = models.TextField(verbose_name=u'答案')
    up_count = models.PositiveIntegerField(verbose_name=u'赞成数')
    down_count = models.PositiveIntegerField(verbose_name=u'反对数')
    comment_count = models.PositiveIntegerField(verbose_name=u'评论数')
    mark_count = models.PositiveIntegerField(verbose_name=u'标记数')
    ranking_weight = models.IntegerField(verbose_name=u'权重')
    created_by = models.ForeignKey(User, related_name='answers', verbose_name=u'创建人')
    created_at = models.DateTimeField(verbose_name=u'创建时间')
    last_updated_by = models.ForeignKey(User, verbose_name=u'最后更新人')
    last_updated_at = models.DateTimeField(verbose_name=u'最后更新时间')
    deleted = models.BooleanField(verbose_name=u'是否被删除')

    class Meta:
        db_table = 'zhidewen_answers'


class Vote(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=u'', related_name='')
    object_pk = models.TextField()
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    value = models.IntegerField(verbose_name=u'值')
    voted_by = models.ForeignKey(User, verbose_name=u'投票人')
    voted_at = models.DateTimeField(verbose_name=u'投票时间')

    class Meta:
        db_table = 'zhidewen_votes'

