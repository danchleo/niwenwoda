#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.models import Question, User, Answer


class ModelTestCase(TestCase):

    def create_user(self, username, *args):
        if not args:
            args = ('%s@zhidewen.com' % username, username)
        return User.objects.create_user(username, *args)

    def create_question(self, *args, **kwargs):
        return Question.objects.create_question(self.user, *args, **kwargs)

    def answer_question(self, *args, **kwargs):
        return Answer.objects.answer_question(self.user, self.q, *args, **kwargs)

    def reload(self, obj):
        return obj.__class__._base_manager.get(pk=obj.pk)