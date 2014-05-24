#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.models import Vote, Question, User


class TestVote(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@zhidewen.com', 'test')
        self.question_pk = Question.objects.create(self.user, 'Foo', 'Bar').pk

    @property
    def question(self):
        return Question.objects.get(pk=self.question_pk)

    def assertVoteCount(self, up, down):
        q = self.question
        self.assertEqual(q.up_count, up)
        self.assertEqual(q.down_count, down)

    def test_vote_by_same_user(self):
        Vote.objects.vote(self.user, self.question, 1)
        self.assertVoteCount(1, 0)

        Vote.objects.vote(self.user, self.question, -1)
        self.assertVoteCount(0, 1)

        Vote.objects.vote(self.user, self.question, 0)
        self.assertVoteCount(0, 0)

    def test_vote_by_many_user(self):
        user_a = User.objects.create_user('test_a', 'test_b@zhidewen.com', 'test_a')
        user_b = User.objects.create_user('test_b', 'test_b@zhidewen.com', 'test_b')

        Vote.objects.vote(user_a, self.question, 1)
        Vote.objects.vote(user_b, self.question, 1)
        self.assertVoteCount(2, 0)

        Vote.objects.vote(user_a, self.question, -1)
        self.assertVoteCount(1, 1)

        Vote.objects.vote(user_a, self.question, 0)
        self.assertVoteCount(1, 0)

