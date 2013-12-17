#-*- encoding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.db.models import query
from django.contrib.auth.models import User
from zhidewen.models import signals


class QuerySet(query.QuerySet):

    def existed(self):
        return self.filter(deleted=False)

    @classmethod
    def as_manager(cls):
        class Manager(models.Manager):
            def get_queryset(self):
                return cls(self.model, using=self._db)

            def __getattr__(self, name):
                try:
                    return getattr(self.get_queryset(), name)
                except AttributeError:
                    return super(Manager, self).__getattr__(name)

            @classmethod
            def existed_manager(mgr, *args, **kwargs):
                class ExistedManager(mgr):
                    def get_queryset(self):
                        return super(ExistedManager, self).get_queryset().existed()
                return ExistedManager(*args, **kwargs)

        return Manager


class ContentModel(models.Model):
    up_count = models.PositiveIntegerField(default=0, verbose_name=u'赞成数')
    down_count = models.PositiveIntegerField(default=0, verbose_name=u'反对数')
    comment_count = models.PositiveIntegerField(default=0, verbose_name=u'评论数')
    mark_count = models.PositiveIntegerField(default=0, verbose_name=u'标记数')
    ranking_weight = models.IntegerField(default=0, verbose_name=u'权重')

    created_by = models.ForeignKey(User, related_name='%(class)ss', verbose_name=u'创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    last_updated_by = models.ForeignKey(User, verbose_name=u'最后更新人')
    last_updated_at = models.DateTimeField(auto_now_add=True, verbose_name=u'最后更新时间')

    deleted = models.BooleanField(default=False, verbose_name=u'是否被删除')

    class Meta:
        abstract = True

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.pk)

    def save(self, *args, **kwargs):
        self.ranking_weight = self.count_ranking()
        return super(ContentModel, self).save(*args, **kwargs)

    def update(self, user, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.last_updated_by = user
        self.last_updated_at = timezone.now()
        return self.save()

    def soft_delete(self):
        if not self.deleted:
            self.deleted = True
            self.save()
            signals.delete_content.send(self.__class__, instance=self)

    def delete(self, using=None):
        self.soft_delete()
        return super(ContentModel, self).delete(using=using)

    def count_ranking(self):
        return 0
