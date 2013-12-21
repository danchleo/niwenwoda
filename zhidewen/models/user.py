#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save


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

def create_user_profile(sender, instance, created, **kwargs):
    """
    创建用户的时同时创建相关的 UserProfile
    """
    if created:

        # 刚注册的用户默认的用户组
        # 系统初始用户组：admin、common_user、newbie
        default_group = Group.objects.filter(name=u'newbie')

        fields = Profile._meta.get_all_field_names()
        related_profile = Profile(user=instance)
        related_profile.__dict__.update({
            field:kwargs[field] for field in fields if field in kwargs
        })

        if default_group and related_profile.group == None:
            related_profile.group = default_group[0]

        related_profile.save()
        
post_save.connect(create_user_profile, sender=User)