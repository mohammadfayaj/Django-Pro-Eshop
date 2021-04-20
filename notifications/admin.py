''' Django notifications admin file '''
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    fields = (
		('unread','public','deleted','emailed',),
		('image'),('level'),('recipient'),('attach_url'),('actor_content_type'),('actor_object_id'),('verb'),('description'),
		('target_object_id'),('target_content_type'),('action_object_content_type'),('action_object_object_id'),
		('timestamp'),
		('notification_slug'),#('data')

        )

    # raw_id_fields = ('',) # to display manytomany field in rew mood
    list_display = ('actor', 'verb', 'level', 'target', 'unread', 'public')
    list_filter = ('level', 'unread', 'public', 'timestamp',)

    def get_queryset(self, request):
        qs = super(NotificationAdmin, self).get_queryset(request)
        return qs.prefetch_related('actor')


admin.site.register(Notification, NotificationAdmin)
