#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'名称')
    icon = models.URLField(blank=True, verbose_name=u'图标')
    description = models.TextField(blank=True, verbose_name=u'描述')
    used_count = models.PositiveIntegerField(default=0, verbose_name=u'使用次数')
    created_by = models.ForeignKey(User, related_name='created_tags', verbose_name=u'创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    deleted = models.BooleanField(default=False, verbose_name=u'是否被删除')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_tags'
