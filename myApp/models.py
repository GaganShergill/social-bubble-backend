from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .storage import OverwriteStorage
from django.conf import settings

import os


# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    eventName = models.CharField(max_length=50)
    eventType = models.CharField(max_length=30)
    venue = models.CharField(max_length=100)
    price = models.IntegerField()
    detail = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now)
    objects = models.Manager()

    def __str__(self):
        return self.eventName


class Activity(models.Model):
    class Meta:
        verbose_name_plural = "Activities"

    id = models.AutoField(primary_key=True)
    activityName = models.CharField(max_length=50)
    activityType = models.CharField(max_length=30)
    venue = models.CharField(max_length=100)
    price = models.IntegerField()
    detail = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now)
    objects = models.Manager()

    def __str__(self):
        return self.activityName


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    destination = models.CharField(max_length=50)
    nights = models.IntegerField()
    price = models.IntegerField()
    detail = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    objects = models.Manager()

    def __str__(self):
        return self.destination


class User(AbstractBaseUser, PermissionsMixin):

    def get_upload_dir(self, filename):
        name = self.email.split('@')[0]
        file_ext = os.path.splitext(filename)[1]
        return f'avatars/{name}{file_ext}'

    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    avatar = models.ImageField(upload_to=get_upload_dir, storage=OverwriteStorage(), null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_avatar_url(self):
        """
        Returns the avatar url for the user.
        """
        if self.avatar:
            return self.avatar. url
        else:
            return settings.MEDIA_URL + 'avatars/default_avatar.png'
