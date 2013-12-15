#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.models import Question, User


class TestQuestion(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@zhidewen.com', 'test')

    def test_create_question(self):
        question = Question.objects.create_question(self.user, 'Foo', 'Bar')

        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(list(self.user.questions.all()), [question])

    def test_count_ranking_when_create_or_update_question(self):
        question = Question.objects.create_question(self.user, 'Foo', 'Bar', view_count=100, answer_count=5)

        self.assertEqual(question.ranking_weight, 125)

        question.view_count += 10
        question.answer_count += 1
        question.save()
        self.assertEqual(question.ranking_weight, 140)

