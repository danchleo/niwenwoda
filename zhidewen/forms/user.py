#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import forms as auth_forms
from zhidewen.models.user import User


class RegisterForm(auth_forms.UserCreationForm):
    """
    注册
    """
    email = forms.EmailField()
    nickname = forms.CharField(max_length=32)

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class ProfileForm(forms.Form):
    """
    个人信息设置
    """
    pass
