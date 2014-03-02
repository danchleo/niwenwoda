#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import forms as auth_forms
from zhidewen.models.user import User
from django.utils.translation import ugettext, ugettext_lazy as _


class RegisterForm(auth_forms.UserCreationForm):
    """
    注册
    """

    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField()
    nickname = forms.CharField(max_length=32, required=False)

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        return self._clean_unique_field('username')

    def clean_email(self):
        return self._clean_unique_field('email')

    def _clean_unique_field(self, name):
        value = self.cleaned_data[name]
        try:
            User._default_manager.get(**{name: value})
        except User.DoesNotExist:
            return value
        raise forms.ValidationError(
            self.error_messages['duplicate_%s' % name],
            code='duplicate_%s' % name,
        )


class ProfileForm(forms.Form):
    """
    个人信息设置
    """
    pass
