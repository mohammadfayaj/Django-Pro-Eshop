''' Django notifications apps file '''
# -*- coding: utf-8 -*-
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = "notifications"

    def ready(self):
        super(NotificationsConfig, self).ready()
        # this is for backwards compability
        import notifications.signals
        notifications.notify = notifications.signals.notify
