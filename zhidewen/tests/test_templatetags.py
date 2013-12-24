#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.templatetags.timeago import timeago
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