#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='account', verbose_name=u'用户')
    nickname = models.CharField(max_length=100, verbose_name=u'昵称')
    birthday = models.DateField(verbose_name=u'出生日期')
    location = models.CharField(max_length=100, verbose_name=u'所在地')
    gender = models.CharField(max_length=10, verbose_name=u'性别')
    about = models.TextField(verbose_name=u'个人简介')
    website = models.URLField(verbose_name=u'个人网站')
    email_is_verified = models.BooleanField(verbose_name=u'邮箱地址是否已验证')

    class Meta:
        app_label = 'zhidewen'
        db_table = 'auth_user_profile'
