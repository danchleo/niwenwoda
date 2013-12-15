#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Vote(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=u'', related_name='')
    object_pk = models.TextField()
    content_object = generic.GenericForeignKey("content_type", "object_pk")
    value = models.IntegerField(verbose_name=u'值')
    voted_by = models.ForeignKey(User, verbose_name=u'投票人')
    voted_at = models.DateTimeField(auto_now=True, verbose_name=u'投票时间')

    class Meta:
        db_table = 'zhidewen_votes'
        unique_together = (('content_type', 'object_pk', 'voted_by'), )
