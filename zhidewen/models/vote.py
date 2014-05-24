#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from zhidewen.models.user import User


class VoteManager(models.Manager):

    def vote(self, user, obj, value):
        """
        投票
        @param user: 投票人
        @param obj: 被投票对象
        @param value: 0 为取消投票
        """

        if value not in Vote.valid_values:
            return False

        content_type = ContentType.objects.get_for_model(obj)
        try:
            vote = self.get(content_type=content_type, voted_by=user)
            if vote.value == value:
                return vote
        except self.model.DoesNotExist:
            vote = self.model(content_type=content_type, voted_by=user, value=0)

        #model = obj.__class__
        #content_type = ContentType.objects.get_for_model(model)

        #try:
        #    vote = self.get(content_type=content_type, object_pk=obj.id, voted_by=user)
        #except self.model.DoesNotExist:
        #    vote = self.model(content_object=obj, voted_by=user, value=0)

        old_value, vote.value = vote.value, value
        vote.save()
        self._update_vote_count(obj, old_value, value)

        return vote

    @staticmethod
    def _update_vote_count(obj, before, after):
        if before not in Vote.valid_values or after not in Vote.valid_values or before == after:
            return
        if before == 1:
            obj.up_count -= 1
        elif before == -1:
            obj.down_count -= 1
        if after == 1:
            obj.up_count += 1
        elif after == -1:
            obj.down_count += 1
        return obj.save()


class Vote(models.Model):
    objects = VoteManager()
    valid_values = [-1, 0, 1]

    content_type = models.ForeignKey(ContentType)
    object_pk = models.TextField()
    content_object = generic.GenericForeignKey("content_type", "object_pk")

    value = models.IntegerField(verbose_name=u'值')
    voted_by = models.ForeignKey(User, verbose_name=u'投票人')
    voted_at = models.DateTimeField(auto_now=True, verbose_name=u'投票时间')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_votes'
        unique_together = (('content_type', 'object_pk', 'voted_by'), )


def vote(self, obj, value):
    pass

from zhidewen.models import User
User.vote = vote
