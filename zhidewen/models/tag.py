#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


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
        app_label = 'zhidewen'
        db_table = 'zhidewen_tags'
