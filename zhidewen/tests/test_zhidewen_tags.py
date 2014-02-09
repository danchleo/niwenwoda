#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.templatetags.zhidewen_tags import timeago, PaginationNode
import datetime


class TestTimeAgo(TestCase):

    def assertTimeAgo(self, expect, date_str, date_now_str):
        p = lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(expect, timeago(p(date_str), p(date_now_str)))

    def test_recent_date(self):
        self.assertTimeAgo(u'刚刚', '2013-01-01 00:00:00', '2013-01-01 00:00:00')
        self.assertTimeAgo(u'刚刚', '2013-01-01 00:00:00', '2013-01-01 00:00:05')
        self.assertTimeAgo(u'6秒前', '2013-01-01 00:00:00', '2013-01-01 00:00:06')
        self.assertTimeAgo(u'59秒前', '2013-01-01 00:00:00', '2013-01-01 00:00:59')
        self.assertTimeAgo(u'1分钟前', '2013-01-01 00:00:00', '2013-01-01 00:01:00')
        self.assertTimeAgo(u'59分钟前', '2013-01-01 00:00:00', '2013-01-01 00:59:59')
        self.assertTimeAgo(u'1小时前', '2013-01-01 00:00:00', '2013-01-01 01:00:00')
        self.assertTimeAgo(u'23小时前', '2013-01-01 00:00:00', '2013-01-01 23:59:59')
        self.assertTimeAgo(u'1天前', '2013-01-01 00:00:00', '2013-01-02 00:00:00')
        self.assertTimeAgo(u'6天前', '2013-01-01 00:00:00', '2013-01-07 23:59:59')
        self.assertTimeAgo(u'1月1日', '2013-01-01 00:00:00', '2013-01-08 00:00:00')
        self.assertTimeAgo(u'2012年12月31日', '2012-12-31 00:00:00', '2013-01-08 00:00:00')
        self.assertTimeAgo(u'2014年1月1日', '2014-1-1 00:00:00', '2013-01-01 00:00:00')


class TestBootstrapPagination(TestCase):

    def assertPagination(self, expect, current_page, page_count, range_length=5, end_length=1):
        actual = PaginationNode.get_page_range(current_page, page_count, range_length, end_length)
        self.assertEqual(expect, actual)

    def assertPaginationLength4(self, expect, current_page, page_count):
        self.assertPagination(expect, current_page, page_count, range_length=4)

    def assertEndLength(self, expect, current_page, page_count):
        self.assertPagination(expect, current_page, page_count, end_length=2)

    def test_pagination(self):
        self.assertPagination([1, 2, 3], 1, 3)

        self.assertPagination([1, 2, 3, 4, 5, 6], 1, 6)

        self.assertPagination([1, 2, 3, 4, 5, '...', 7], 1, 7)
        self.assertPagination([1, 2, 3, 4, 5, '...', 7], 3, 7)
        self.assertPagination([1, 2, 3, 4, 5, 6, 7], 4, 7)
        self.assertPagination([1, '...', 3, 4, 5, 6, 7], 5, 7)
        self.assertPagination([1, '...', 3, 4, 5, 6, 7], 7, 7)

        self.assertPagination([1, 2, 3, 4, 5, 6, '...', 9], 4, 9)
        self.assertPagination([1, '...', 3, 4, 5, 6, 7, '...', 9], 5, 9)

    def test_pagination_end_length(self):
        self.assertEndLength([1, 2, 3, 4, 5, 6, 7], 1, 7)
        self.assertEndLength([1, 2, 3, 4, 5, '...', 7, 8], 1, 8)
        self.assertEndLength([1, 2, '...', 4, 5, 6, 7, 8], 8, 8)
        self.assertEndLength([1, 2, 3, 4, 5, 6, 7, 8, 9], 5, 9)
        self.assertEndLength([1, 2, '...', 4, 5, 6, 7, 8, '...', 10, 11], 6, 11)

    def test_pagination_length_4(self):
        self.assertPaginationLength4([1, 2, 3], 1, 3)

        self.assertPaginationLength4([1, 2, 3, 4, 5], 1, 5)

        self.assertPaginationLength4([1, 2, 3, 4, '...', 6], 1, 6)
        self.assertPaginationLength4([1, 2, 3, 4, '...', 6], 2, 6)
        self.assertPaginationLength4([1, 2, 3, 4, 5, 6], 3, 6)
        self.assertPaginationLength4([1, '...', 3, 4, 5, 6], 4, 6)
        self.assertPaginationLength4([1, '...', 3, 4, 5, 6], 6, 6)

        self.assertPaginationLength4([1, '...', 3, 4, 5, 6, '...', 8], 4, 8)
