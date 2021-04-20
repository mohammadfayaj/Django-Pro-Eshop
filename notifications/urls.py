''' Django notification urls file '''
# -*- coding: utf-8 -*-
from distutils.version import StrictVersion  # pylint: disable=no-name-in-module,import-error
from django.urls import path
from django import get_version
from django.conf.urls.static import static
from django.conf import settings
from . import views

if StrictVersion(get_version()) >= StrictVersion('2.0'):
    from django.urls import re_path as pattern
else:
    from django.conf.urls import url as pattern


urlpatterns = [
    pattern(r'^$', views.AllNotificationsList.as_view(), name='all'),
    path('hide-notification/<notification_slug>/', views.hide_notification, name='hide_notification'),
    pattern(r'^unread/$', views.UnreadNotificationsList.as_view(), name='unread'),
    pattern(r'^mark-all-as-read/$', views.mark_all_as_read, name='mark_all_as_read'),
    # pattern(r'^mark-all-as-read-in-admin/$', views.mark_all_as_read_in_admin, name='mark_all_as_read_admin'),
    pattern(r'^mark-as-read/(?P<slug>\d+)/$', views.mark_as_read, name='mark_as_read'),
    pattern(r'^mark-as-unread/(?P<slug>\d+)/$', views.mark_as_unread, name='mark_as_unread'),
    pattern(r'^delete/(?P<slug>\d+)/$', views.delete, name='delete'),
    pattern(r'^api/unread_count/$', views.live_unread_notification_count, name='live_unread_notification_count'),
    pattern(r'^api/all_count/$', views.live_all_notification_count, name='live_all_notification_count'),
    pattern(r'^api/unread_list/$', views.live_unread_notification_list, name='live_unread_notification_list'),
    pattern(r'^api/all_list/', views.live_all_notification_list, name='live_all_notification_list'),
] 

app_name = 'notifications'
