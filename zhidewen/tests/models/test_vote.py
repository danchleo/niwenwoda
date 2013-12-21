#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.models import Vote, Question, User


class TestVote(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@zhidewen.com', 'test')
        self.question = Question.objects.create(self.user, 'Foo', 'Bar')

    def reload_question(self):
        return Question.objects.get(pk=self.question.pk)

    def assertVoteCount(self, up, down):
        q = self.reload_question()
        self.assertEqual(q.up_count, up)
        self.assertEqual(q.down_count, down)

    def test_add_vote(self):
        Vote.objects.vote(self.user, self.question, 1)
        self.assertVoteCount(1, 0)

        Vote.objects.vote(self.user, self.question, -1)
        self.assertVoteCount(0, 1)

        Vote.objects.vote(self.user, self.question, 0)
        self.assertVoteCount(0, 0)
