#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('mysite.apps.account.views',
    (r'^login/?$',                  'login'),
    (r'^logout/?$',                 'logout'),
    (r'^signup/?$',                 'signup'),
    (r'^clients/?$',                'clients'),
)