#-*- encoding: utf-8 -*-

from django.dispatch import Signal

delete_content = Signal(providing_args=['instance'])
create_content = Signal(providing_args=['instance'])
