#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from zhidewen.models.question import Question
from zhidewen.models.answer import Answer


class MarkManager(models.Manager):

    def mark(self, user, obj):
        model = obj.__class__
        content_type = ContentType.objects.get_for_model(model)

        mark, created = self.get_or_create(content_type=content_type, object_pk=obj.id, marked_by=user)

        if created:
            obj.mark_count += 1
            obj.save()

        return mark

    def question_marks(self, user):
        return self._type_marks(user, Question)

    def answer_marks(self, user):
        return self._type_marks(user, Answer)

    def _type_marks(self, user, model):
        content_type = ContentType.objects.get_for_model(model)
        return content_type.marks.filter(marked_by=user)

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
