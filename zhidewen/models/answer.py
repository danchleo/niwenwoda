#-*- encoding: utf-8 -*-

from django.db import models
from zhidewen.models import base
from zhidewen.models.question import Question
from zhidewen.models import signals


class AnswerQuerySet(base.QuerySet):

    def best(self):
        return self.order_by('-ranking_weight')

    def oldest(self):
        return self.order_by('created_at')


class AnswerManager(AnswerQuerySet.as_manager()):

    def answer_question(self, user, question, content, **kwargs):
        answer = self.create(content=content, question=question, created_by=user, last_updated_by=user, **kwargs)
        signals.create_content.send(answer.__class__, instance=answer)
        return answer


class Answer(base.ContentModel):
    objects = AnswerManager()
    exsited = AnswerManager.existed_manager()

    question = models.ForeignKey(Question, related_name='answers', verbose_name=u'问题')
    content = models.TextField(verbose_name=u'答案')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_answers'

    def count_ranking(self):
        return self.up_count - self.down_count


def up_answer_count(instance, **kwargs):
    instance.question.answer_count += 1
    instance.question.save()

def down_answer_count(instance, **kwargs):
    instance.question.answer_count -= 1
    instance.question.save()


signals.delete_content.connect(down_answer_count, sender=Answer)
signals.create_content.connect(up_answer_count, sender=Answer)



