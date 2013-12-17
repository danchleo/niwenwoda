#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.tests.models.base import ModelTestCase
from zhidewen.models import Answer
from django.utils import timezone


class TestAnswer(ModelTestCase):

    def setUp(self):
        self.user = self.create_user('test')
        self.q = self.create_question('Foo', 'Bar')

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
        answer.update(edit_user, content='Content')

        new_answer = Answer.objects.get(pk=answer.id)
        self.assertTrue(new_answer.last_updated_at > last_updated_at)
        self.assertEqual(edit_user, new_answer.last_updated_by)

        last_updated_at = new_answer.last_updated_at
        new_answer.title = 'FOO'
        new_answer.save()
        self.assertEqual(new_answer.last_updated_at, last_updated_at)


class TestListAnswer(ModelTestCase):

    def setUp(self):
        self.user = self.create_user('test')
        self.q = self.create_question('Foo', 'Bar')

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


class TestAnswerCount(ModelTestCase):

    def setUp(self):
        self.user = self.create_user('test')
        self.q = self.create_question('Foo', 'Bar')
        self.answer = self.answer_question('A')
        self.assertEqual(1, self.q.answer_count)

    def test_answer_count(self):
        self.answer.soft_delete()
        self.assertEqual(0, self.q.answer_count)

    def test_answer_count_hard_delete(self):
        self.answer.delete()
        self.assertEqual(0, self.q.answer_count)

    def xtest_answer_count_query_set_delete(self):
        self.q.answers.delete()
        self.assertEqual(0, self.q.answer_count)

    def test_answer_count_soft_and_hard_delete(self):
        self.answer.soft_delete()
        self.assertEqual(0, self.q.answer_count)

        self.answer.delete()
        self.assertEqual(0, self.q.answer_count)


class TestRefreshQuestion(ModelTestCase):

    def test(self):
        self.user = self.create_user('test')
        self.q = self.create_question('Foo', 'Bar')
        last_refreshed_at = self.q.last_refreshed_at
        self.answer_question('A')
        self.assertTrue(self.q.last_refreshed_at > last_refreshed_at)
