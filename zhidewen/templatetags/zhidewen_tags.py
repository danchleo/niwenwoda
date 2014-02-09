# -*- coding: utf-8 -*-

from django import template
from django.utils import timezone
from django.template.loader import get_template
from zhidewen.models import Question
import datetime

register = template.Library()


@register.filter(name='timeago')
def timeago(date, now=None):
    """
    格式化日期为相对时间
        如 ‘1分钟前', '5天前', '12月12日'
    """
    if not now:
        now = timezone.now()
    timedelta = now - date
    if timedelta >= datetime.timedelta(seconds=0):
        if timedelta.days < 1:
            seconds = timedelta.seconds
            if seconds <= 5:
                return u'刚刚'
            if seconds < 60:
                return u'%s秒前' % seconds
            if seconds < 3600:
                return u'%s分钟前' % (seconds/60)
            return u'%s小时前' % (seconds/3600)
        if timedelta.days < 7:
            return u'%s天前' % timedelta.days
    # strptime 不支持 unicode，故此处用 %
    if date.year == now.year:
        return u'%s月%s日' % (date.month, date.day)
    return u'%s年%s月%s日' % (date.year, date.month, date.day)


MORE_PAGE_SYMBOL = '...'


class PaginationNode(template.Node):

    def __init__(self, page):
        self.page = template.Variable(page)

    def render(self, context):
        try:
            page = self.page.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        last_page = page.paginator.num_pages

        if last_page <= 1:
            return ''
        page_range = self.get_page_range(page.number, last_page)
        page_range = [('#' if n == MORE_PAGE_SYMBOL else '?page=%s' % n, n) for n in page_range]
        context = template.Context({'page': page, 'page_range': page_range}, autoescape=False)
        return get_template('includes/pagination.html').render(context)

    @staticmethod
    def get_page_range(current_page, page_count, range_length=5, end_length=1):
        """
        分页样式标签
            至少显示 length 个分页，且始终显示第一页和最后一页
            使用方式:
                {% bootstrap_paginate page %}
        """

        range_space = range_length - 1

        min_range = max(min(current_page - range_space/2, page_count - range_space), 1)
        max_range = min(min_range + range_space, page_count)

        head_range = range(1, 1 + end_length) + [MORE_PAGE_SYMBOL]
        tail_range = [MORE_PAGE_SYMBOL] + range(page_count - end_length + 1, page_count + 1)

        page_range = head_range[:min_range - 1] + range(min_range, max_range + 1)
        if page_count > max_range:
            page_range += tail_range[-(page_count - max_range):]
        return page_range


@register.tag
def bootstrap_paginate(parser, token):
    try:
        tag_name, page = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    return PaginationNode(page)


@register.simple_tag
def active(request, pattern):
    import re
    current_page = False
    if pattern == '/':
        current_page = pattern == request.path
    elif re.search(pattern, request.path):
        current_page = True
    return current_page and 'active' or ''


@register.simple_tag
def answered_count():
    return Question.existed.answered().count()


@register.simple_tag
def unanswered_count():
    return Question.existed.unanswered().count()