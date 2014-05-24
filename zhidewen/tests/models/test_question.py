#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.models import Question, User, Tag
from django.utils import timezone
from zhidewen.tests.models.base import ModelTestCase


class TestQuestion(ModelTestCase):

    def setUp(self):
        self.user = self.create_user('test')

    def test_create_question(self):
        question = Question.objects.create(self.user, 'Foo', 'Bar')

        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(list(self.user.questions.all()), [question])

    def test_ranking_weight(self):
        question = self.create_question('Foo', 'Bar', view_count=100, answer_count=5)

        self.assertEqual(question.ranking_weight, 125)

        question.view_count += 10
        question.answer_count += 1
        question.save()
        self.assertEqual(question.ranking_weight, 140)

    def test_update(self):
        question = self.create_question('Foo', 'Bar')
        last_updated_at = question.last_updated_at
        edit_user = User.objects.create_user('admin', 'admin@zhidewen.com', 'admin')
        question.update(edit_user, title='foo', content='bar')

        new_question = Question.objects.get(pk=question.id)
        self.assertTrue(new_question.last_updated_at > last_updated_at)
        self.assertEqual(edit_user, new_question.last_updated_by)

        last_updated_at = new_question.last_updated_at
        new_question.title = 'FOO'
        new_question.save()
        self.assertEqual(new_question.last_updated_at, last_updated_at)


class TestListQuestion(ModelTestCase):

    def setUp(self):
        self.user = self.create_user('test')

        self.q1 = self.create_question('Q1', 'Q1', answer_count=1)
        self.q2 = self.create_question('Q2', 'Q2', view_count=100)
        self.q3 = self.create_question('Q3', 'Q3')

        self.q2.last_refreshed_at = timezone.now()
        self.q2.save()

    def test_newest_list(self):
        self.assertEqual(list(Question.objects.newest()), [self.q2, self.q3, self.q1])

    def test_hottest_list(self):
        self.assertEqual(list(Question.objects.hottest()), [self.q2, self.q1, self.q3])

    def test_unanswered_list(self):
        self.assertEqual(list(Question.objects.unanswered().recent()), [self.q3, self.q2])

        self.q3.closed = True
        self.q3.save()
        self.assertEqual(list(Question.objects.unanswered()), [self.q2])

    def test_answered_count(self):
        self.assertEqual(1, Question.objects.answered().count())

    def test_existed_manager_and_soft_delete(self):
        self.assertEqual(list(Question.objects.newest()), [self.q2, self.q3, self.q1])
        self.q2.soft_delete()
        self.assertEqual(list(Question.existed.newest()), [self.q3, self.q1])
        self.assertEqual(list(Question.objects.newest()), [self.q2, self.q3, self.q1])


class TestQuestionTag(ModelTestCase):

    def setUp(self):
        self.user = self.create_user('test')

    def test_create_question_with_tag_names(self):
        question = Question.objects.create(self.user, 'Foo', 'Foo', tag_names=['foo', 'bar'])
        tags = Question.objects.get(pk=question.id).tags.all()
        self.assertEqual([t.name for t in tags], ['foo', 'bar'])

    def test_create_question_with_existed_tag_name(self):
        Tag.objects.create(created_by=self.user, name='foo')
        question = Question.objects.create(self.user, 'Foo', 'Foo', tag_names=['foo', 'bar'])
        tags = Question.objects.get(pk=question.id).tags.all()
        self.assertEqual([t.name for t in tags], ['foo', 'bar'])
        self.assertEqual(Tag.objects.count(), 2)

    def test_add_and_remote_tag(self):
        q = self.create_question('Foo', 'Bar')
        q.add_tag(self.user, 'foo')

        tag = Tag.objects.first()

        self.assertEqual(Question.objects.get(pk=q.id).tags.count(), 1)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(tag.used_count, 1)
        self.assertEqual(tag.name, 'foo')

        q.remove_tag(tag)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(tag.used_count, 0)

        self.assertEqual(Question.objects.get(pk=q.id).tags.count(), 0)
