#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',)#-*- coding: utf-8 -*-


from django.conf.urls import patterns, url


urlpatterns = patterns('mysite.apps.client.views',
    (r'^(?P<client_id>\w+)/?$',            'client'),
)# Create your views here.
