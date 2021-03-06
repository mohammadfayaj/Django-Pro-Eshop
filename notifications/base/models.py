''' Django notifications models file '''
# -*- coding: utf-8 -*-
# pylint: disable=too-many-lines
from distutils.version import StrictVersion  # pylint: disable=no-name-in-module,import-error
import copy

from django import get_version
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from jsonfield.fields import JSONField
from model_utils import Choices

from notifications import settings as notifications_settings
from notifications.signals import notify
from notifications.utils import id2slug
from swapper import load_model
from notifications.utils import id2slug

if StrictVersion(get_version()) >= StrictVersion('1.8.0'):
    from django.contrib.contenttypes.fields import GenericForeignKey  # noqa
else:
    from django.contrib.contenttypes.generic import GenericForeignKey  # noqa


EXTRA_DATA = notifications_settings.get_config()['USE_JSONFIELD']


def is_soft_delete():
    return notifications_settings.get_config()['SOFT_DELETE']


def assert_soft_delete():
    if not is_soft_delete():
        msg = """To use 'deleted' field, please set 'SOFT_DELETE'=True in settings.
        Otherwise NotificationQuerySet.unread and NotificationQuerySet.read do NOT filter by 'deleted' field.
        """
        raise ImproperlyConfigured(msg)


class NotificationQuerySet(models.query.QuerySet):
    ''' Notification QuerySet '''
    def unsent(self):
        return self.filter(emailed=False)

    def sent(self):
        return self.filter(emailed=True)

    def unread(self, include_deleted=False):
        """Return only unread items in the current queryset"""
        if is_soft_delete() and not include_deleted:
            return self.filter(unread=True, deleted=False)

        # When SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
        # In this case, to improve query performance, don't filter by 'deleted' field
        return self.filter(unread=True)

    def read(self, include_deleted=False):
        """Return only read items in the current queryset"""
        if is_soft_delete() and not include_deleted:
            return self.filter(unread=False, deleted=False)

        # When SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
        # In this case, to improve query performance, don't filter by 'deleted' field
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset.
        Optionally, filter these by recipient first.
        """
        # We want to filter out read ones, as later we will store
        # the time they were marked as read.
        qset = self.unread(True)
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset.
        Optionally, filter these by recipient first.
        """
        qset = self.read(True)

        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=True)

    def deleted(self):
        """Return only deleted items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=True)

    def active(self):
        """Return only active(un-deleted) items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=False)

    def mark_all_as_deleted(self, recipient=None):
        """Mark current queryset as deleted.
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qset = self.active()
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(deleted=True)

    def mark_all_as_active(self, recipient=None):
        """Mark current queryset as active(un-deleted).
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qset = self.deleted()
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(deleted=False)

    def mark_as_unsent(self, recipient=None):
        qset = self.sent()
        if recipient:
            qset = qset.filter(recipient=recipient)
        return qset.update(emailed=False)

    def mark_as_sent(self, recipient=None):
        qset = self.unsent()
        if recipient:
            qset = qset.filter(recipient=recipient)
        return qset.update(emailed=True)


class AbstractNotification(models.Model):
    """
    Action model describing the actor acting out a verb (on an optional
    target).
    Nomenclature based on http://activitystrea.ms/specs/atom/1.0/
    Generalized Format::
        <actor> <verb> <time>
        <actor> <verb> <target> <time>
        <actor> <verb> <action_object> <target> <time>
    Examples::
        <justquick> <reached level 60> <1 minute ago>
        <brosner> <commented on> <pinax/pinax> <2 hours ago>
        <washingtontimes> <started follow> <justquick> <8 minutes ago>
        <mitsuhiko> <closed> <issue 70> on <mitsuhiko/flask> <about 2 hours ago>
    Unicode Representation::
        justquick reached level 60 1 minute ago
        mitsuhiko closed issue 70 on mitsuhiko/flask 3 hours ago
    HTML Representation::
        <a href="http://oebfare.com/">brosner</a> commented on <a href="http://github.com/pinax/pinax">pinax/pinax</a> 2 hours ago # noqa
    """
    LEVELS = Choices('success', 'info', 'warning', 'error')
    level = models.CharField(choices=LEVELS, default=LEVELS.info, max_length=20,help_text='Notifications Background Color')

    recipient = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='notifications',
        # on_delete=models.CASCADE,
        help_text='Your Customer, Who You Gonna Send Notification!',
    )
    unread = models.BooleanField(default=True, blank=False, db_index=True)

    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor',on_delete=models.CASCADE,help_text='Select- auth | user')
    actor_object_id = models.CharField(max_length=255,help_text='Same As Recipient Field',default=1)
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')

    verb = models.CharField(max_length=255, help_text='Your Notification Title')
    description = models.TextField(blank=True, null=True)

    target_content_type = models.ForeignKey(
        ContentType,
        related_name='notify_target',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    action_object_content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                                   related_name='notify_action_object', on_delete=models.CASCADE)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object = GenericForeignKey('action_object_content_type', 'action_object_object_id')

    timestamp = models.DateTimeField(default=timezone.now)

    public = models.BooleanField(default=True, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    emailed = models.BooleanField(default=False, db_index=True)

    data = JSONField(blank=True, null=True)
    objects = NotificationQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ('-timestamp',)
        app_label = 'notifications'

    def __unicode__(self):
        ctx = {
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object,
            'target': self.target,
            'timesince': self.timesince()
        }
        if self.target:
            if self.action_object:
                return u'%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago' % ctx
            return u'%(actor)s %(verb)s %(target)s %(timesince)s ago' % ctx
        if self.action_object:
            return u'%(actor)s %(verb)s %(action_object)s %(timesince)s ago' % ctx
        return u'%(actor)s %(verb)s %(timesince)s ago' % ctx

    def __str__(self):  # Adds support for Python 3
        return self.__unicode__()

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.timestamp, now)

    @property
    def slug(self):
        return id2slug(self.id)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def notify_handler(verb, **kwargs):
    """
    Handler function to create Notification instance upon action signal call.
    """

    # Pull the options out of kwargs
    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient')
    actor = kwargs.pop('sender')
    optional_objs = [
        (kwargs.pop(opt, None), opt)
        for opt in ('target', 'action_object')
    ]
    public = bool(kwargs.pop('public', True))
    description = kwargs.pop('description', None)
    timestamp = kwargs.pop('timestamp', timezone.now())
    Notification = load_model('notifications', 'Notification')
    level = kwargs.pop('level', Notification.LEVELS.info)

    local_kwargs = locals()

    # Check if User or Group
    if isinstance(recipient, Group):
        recipients = recipient.user_set.all()
    elif isinstance(recipient, (QuerySet, list)):
        recipients = recipient
    else:
        recipients = [recipient]

    new_notifications = []

    GROUP_SIMILAR = notifications_settings.get_config()['GROUP_SIMILAR']
    GROUP_SIMILAR_FIELDS = notifications_settings.get_config()['GROUP_SIMILAR_FIELDS']

    for recipient in recipients:
        if GROUP_SIMILAR:
            copied_fields = copy.deepcopy(GROUP_SIMILAR_FIELDS)

            for k, v in copied_fields.items():
                if isinstance(v, six.string_types) and v.startswith('$'):
                    copied_fields[k] = local_kwargs[v[1:]]

            # Set optional objects
            for obj, opt in optional_objs:
                if obj is not None:
                    copied_fields['%s_object_id' % opt] = obj.pk
                    copied_fields['%s_content_type' % opt] = ContentType.objects.get_for_model(obj)

            oldnotify = Notification.objects.filter(
                recipient=recipient,
                actor_content_type=ContentType.objects.get_for_model(actor),
                actor_object_id=actor.pk,
                verb=text_type(verb)
            ).filter(**copied_fields)

            for n in oldnotify:
                if kwargs and EXTRA_DATA:
                    n.data = kwargs

                n.timestamp = timestamp
                n.description = description
                n.emailed = False
                n.save()

                new_notifications.append(n)

            if len(oldnotify) > 0:
                continue

        newnotify = Notification(
            recipient=recipient,
            actor_content_type=ContentType.objects.get_for_model(actor),
            actor_object_id=actor.pk,
            verb=text_type(verb),
            public=public,
            description=description,
            timestamp=timestamp,
            level=level,
        )

        # Set optional objects
        for obj, opt in optional_objs:
            if obj is not None:
                setattr(newnotify, '%s_object_id' % opt, obj.pk)
                setattr(newnotify, '%s_content_type' % opt,
                        ContentType.objects.get_for_model(obj))

        if kwargs and EXTRA_DATA:
            newnotify.data = kwargs

        newnotify.save()
        new_notifications.append(newnotify)

    return new_notifications


# connect the signal
notify.connect(notify_handler, dispatch_uid='notifications.models.notification')