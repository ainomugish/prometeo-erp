#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2011 Emanuele Bertoldi'
__version__ = '0.0.5'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.conf import settings

class NotificationManager(models.Manager):
    """Manager for notifications.
    """
    def read(self):
        return self.filter(read__isnull=False)

    def unread(self):
        return self.filter(read__isnull=True)

class Signature(models.Model):
    """Signature model.
    """
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    subscribers = models.ManyToManyField('auth.User', null=True, blank=True, through='Subscription', verbose_name=_('subscribers'))

    class Meta:
        verbose_name = _('signature')
        verbose_name_plural = _('signatures')

    def __unicode__(self):
        return self.title
        
class Subscription(models.Model):
    """Subscription model.
    """
    user = models.ForeignKey('auth.User')
    signature = models.ForeignKey(Signature)
    send_email = models.BooleanField(default=True, verbose_name=_('send email'))

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

class Notification(models.Model):
    """Notification model.
    """
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)
    user = models.ForeignKey('auth.User', verbose_name=_('user'))
    signature = models.ForeignKey(Signature, verbose_name=_('signature'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    read = models.DateTimeField(blank=True, null=True, verbose_name=_('read on'))

    objects = NotificationManager()

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ('-created', 'id')
        get_latest_by = '-created'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('notification_detail', (), {"username": self.user.username, "id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('notification_delete', (), {"username": self.user.username, "id": self.pk})

    def clean(self):
        if self.user.subscription_set.filter(signature=self.signature).count() == 0:
            raise ValidationError('The user is not subscribed for this kind of notification.')
        super(Notification, self).clean()

def send_notification_email(sender, instance, signal, *args, **kwargs):
    if Subscription.objects.filter(signature=instance.signature, user=instance.user, send_email=True).count() > 0:
        email_subject = instance.title
        email_body = instance.description
        email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost.com')
        email = EmailMessage(email_subject, email_body, email_from, [instance.user.email,])
        email.content_subtype = "html"
        email.send()

models.signals.post_save.connect(send_notification_email, Notification)