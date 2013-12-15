#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.models import Question, User, Answer
from django.utils import timezone


class BaseAnswerTest(TestCase):

    def setUp(self):
        self.user = self.create_user('test')
        self.q = self.create_question('Foo', 'Bar')

    def create_user(self, username, *args):
        if not args:
            args = ('%s@zhidewen.com' % username, username)
        return User.objects.create_user(username, *args)

    def create_question(self, *args, **kwargs):
        return Question.objects.create_question(self.user, *args, **kwargs)

    def answer_question(self, *args, **kwargs):
        return Answer.objects.answer_question(self.user, self.q, *args, **kwargs)


class TestAnswer(BaseAnswerTest):

    def test_answer_question(self):
        answer = Answer.objects.answer_question(self.user, self.q, 'Content')

        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(list(self.q.answers.all()), [answer])

    def test_ranking_weight(self):
        answer = self.answer_question('Content', up_count=5, down_count=2)
        self.assertEqual(answer.ranking_weight, 3)

        answer.up_count += 2
        answer.save()
        self.assertEqual(answer.ranking_weight, 5)

    def test_update(self):
        answer = self.answer_question('Content')
        edit_user = self.create_user('admin')
        last_updated_at = answer.last_updated_at
        answer.update(edit_user, 'Content')

        new_answer = Answer.objects.get(pk=answer.id)
        self.assertTrue(new_answer.last_updated_at > last_updated_at)
        self.assertEqual(edit_user, new_answer.last_updated_by)

        last_updated_at = new_answer.last_updated_at
        new_answer.title = 'FOO'
        new_answer.save()
        self.assertEqual(new_answer.last_updated_at, last_updated_at)


class ListAnswerTest(BaseAnswerTest):

    def setUp(self):
        super(ListAnswerTest, self).setUp()
        self.a1 = self.answer_question('A1', down_count=2)
        self.a2 = self.answer_question('A2', up_count=5)
        self.a3 = self.answer_question('A3')

    def test_best_list(self):
        self.assertEqual(list(self.q.answers.best()), [self.a2, self.a3, self.a1])

    def test_oldest_list(self):
         self.assertEqual(list(self.q.answers.oldest()), [self.a1, self.a2, self.a3])

    def test_existed_manager_and_soft_delete(self):
        self.assertEqual(list(self.q.answers.oldest()), [self.a1, self.a2, self.a3])
        self.a2.soft_delete()
        self.assertEqual(list(self.q.answers.existed().oldest()), [self.a1, self.a3])
        self.assertEqual(list(self.q.answers.oldest()), [self.a1, self.a2, self.a3])

