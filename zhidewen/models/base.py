#-*- encoding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.db.models import query


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

