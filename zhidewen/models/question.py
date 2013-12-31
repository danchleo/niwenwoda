#-*- encoding: utf-8 -*-

from django.db import models
from zhidewen.models import base
from zhidewen.models import signals
from zhidewen.models.tag import Tag


class QuestionQuerySet(base.QuerySet):

    def newest(self):
        return self.order_by('-last_refreshed_at')

    def hottest(self):
        return self.order_by('-ranking_weight')

    def recent(self):
        return self.order_by('-created_at')

    def unanswered(self):
        return self.filter(answer_count=0, closed=False)

    def answered(self):
        return self.filter(answer_count__gt=0)

    def close(self):
        return self._clone().update({'closed': True})

    def open(self):
        return self._clone().update({'closed': False})

    def related_tags(self):
        return Tag.existed.filter(questions__in=self).most_used()


class QuestionManager(QuestionQuerySet.as_manager()):

    def create(self, user, title, content, tag_names=None, **kwargs):
        question = self.model(title=title, content=content, created_by=user, last_updated_by=user, **kwargs)
        question.save()
        if tag_names:
            for tag_name in tag_names:
                question.add_tag(user, tag_name)

        signals.create_content.send(question.__class__, instance=question)
        return question


class Question(base.ContentModel):
    objects = QuestionManager()
    existed = QuestionManager.existed_manager()

    title = models.CharField(max_length=140, verbose_name=u'标题')
    content = models.TextField(verbose_name=u'补充说明', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name=u'标签')

    view_count = models.PositiveIntegerField(default=0, verbose_name=u'浏览数')
    answer_count = models.PositiveIntegerField(default=0, verbose_name=u'回答数')

    last_refreshed_at = models.DateTimeField(auto_now_add=True, verbose_name=u'最后活跃时间')
    closed = models.BooleanField(default=False, verbose_name=u'是否被关闭')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_questions'

    @property
    def score(self):
        return self.up_count - self.down_count

    @property
    def author(self):
        return self.created_by

    @property
    def summary(self):
        return self.content

    def count_ranking(self):
        return sum([self.answer_count*5,
                    self.up_count*3,
                    self.mark_count*2,
                    self.down_count,
                    self.view_count,
                    self.comment_count])

    def add_tag(self, user, tag_name):
        tag = Tag.objects.get_or_create_by_name(tag_name, user)
        self.tags.add(tag)
        tag.used_count += 1
        tag.save()

    def remove_tag(self, tag):
        self.tags.remove(tag)
        tag.used_count -= 1
        tag.save()

    def close(self):
        self.close = True

    def open(self):
        self.close = False


def create_question(instance, **kwargs):
    instance.created_by.question_count += 1
    instance.created_by.save()


def delete_question(instance, **kwargs):
    instance.created_by.question_count -= 1
    instance.created_by.save()


signals.create_content.connect(create_question, sender=Question)
signals.delete_content.connect(delete_question, sender=Question)
