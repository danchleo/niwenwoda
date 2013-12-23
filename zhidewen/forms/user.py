#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import forms as auth_forms


class RegisterForm(auth_forms.UserCreationForm):
    """
    注册
    """
    pass


class ProfileForm(forms.Form):
    """
    个人信息设置
    """
    pass
