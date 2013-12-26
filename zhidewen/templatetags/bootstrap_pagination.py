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
        return get_template('_pagination.html').render(context)

    @staticmethod
    def get_page_range(cur_page, last_page, length=5):
        """
        分页样式标签
            至少显示 length 个分页，且始终显示第一页和最后一页
            使用方式:
                {% bootstrap_paginate page %}
        """
        dist = length - 1
        left_dist = dist/2
        if last_page <= 1 + dist:
            return range(1, last_page + 1)

        page_range = []

        if cur_page <= 1 + left_dist:
            start_page = 1
        elif cur_page >= last_page - (dist - left_dist):
            start_page = last_page - dist
        else:
            start_page = cur_page - left_dist

        end_page = start_page + dist

        if start_page > 1:
            page_range.append(1)

            if start_page > 2:
                page_range.append(MORE_PAGE_SYMBOL)

        page_range.extend(range(start_page, end_page + 1))

        if end_page < last_page - 1:
            page_range.append(MORE_PAGE_SYMBOL)

        if end_page < last_page:
            page_range.append(last_page)

        return page_range


@register.tag
def bootstrap_paginate(parser, token):
    try:
        tag_name, page = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    return PaginationNode(page)