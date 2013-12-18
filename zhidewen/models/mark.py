#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class MarkManager(models.Manager):

    def mark(self, user, obj):
        model = obj.__class__
        content_type = ContentType.objects.get_for_model(model)

        mark, created = self.get_or_create(content_type=content_type, object_pk=obj.id, marked_by=user)

        if created:
            obj.mark_count += 1
            obj.save()

        return mark


class Mark(models.Model):
    objects = MarkManager()

    content_type = models.ForeignKey(ContentType, related_name='marks')
    object_pk = models.TextField()
    content_object = generic.GenericForeignKey("content_type", "object_pk")
    marked_by = models.ForeignKey(User, related_name='marks', verbose_name=u'标记人')
    marked_at = models.DateTimeField(auto_now_add=True, verbose_name=u'标记时间')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_marks'
        unique_together = (('content_type', 'object_pk', 'marked_by'), )

    def delete(self, using=None):
        self.content_object.mark_count -= 1
        self.content_object.save()
        return super(Mark, self).delete()
