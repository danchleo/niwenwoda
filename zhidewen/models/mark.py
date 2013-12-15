#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Mark(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='marks')
    object_pk = models.TextField()
    content_object = generic.GenericForeignKey("content_type", "object_pk")
    marked_by = models.ForeignKey(User, related_name='marks', verbose_name=u'标记人')
    marked_at = models.DateTimeField(verbose_name=u'标记时间')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_marks'
