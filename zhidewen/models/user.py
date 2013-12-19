#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', verbose_name=u'用户')
    nickname = models.CharField(max_length=100, verbose_name=u'昵称')
    birthday = models.DateField(verbose_name=u'出生日期', null=True, blank=True)
    location = models.CharField(max_length=100, verbose_name=u'所在地', default='', blank=True)
    gender = models.CharField(max_length=10, verbose_name=u'性别')
    about = models.TextField(verbose_name=u'个人简介', null=True, blank=True)
    website = models.URLField(verbose_name=u'个人网站', null=True, blank=True)
    email_is_verified = models.BooleanField(verbose_name=u'邮箱地址是否已验证', default=False, blank=True)

    class Meta:
        app_label = 'zhidewen'
        db_table = 'auth_user_profile'

# 刚注册的用户默认的用户组
# 系统初始用户组：admin、common_user、newbie
default_role = Group.objects.get(name=u'newbie')
def create_user_profile(sender, instance, created, **kwargs):
    """
    创建用户的时同时创建相关的 UserProfile
    """
    if created:
        related_profile = Profile()
        for field in Pofile._meta.get_all_field_names() and field in kwargs:
            attrs[field] = kwargs[field]
        related_profile.__dict__ = attrs
        related_profile.save()
        
post_save.connect(create_user_profile, sender=User)