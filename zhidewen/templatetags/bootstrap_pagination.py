# -*- coding: utf-8 -*-

from django import template
from django.template.loader import get_template


register = template.Library()

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

        return head_range[:min_range - 1] + range(min_range, max_range + 1) + tail_range[len(tail_range) - (page_count - max_range):]


@register.tag
def bootstrap_paginate(parser, token):
    try:
        tag_name, page = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    return PaginationNode(page)