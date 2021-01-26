# -*- coding: utf-8 -*-
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<client_id>\w+)/?$', 'mysite.apps.client.views', 'client'),
]
