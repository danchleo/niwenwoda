#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.models import Question, User


class TestQuestion(TestCase):

    def test_create_question(self):
        user = User.objects.create_user('test', 'test@zhidewen.com', 'test')
        question = Question.objects.create_question(user, 'Foo', 'Bar')

        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(list(user.questions.all()), [question])
