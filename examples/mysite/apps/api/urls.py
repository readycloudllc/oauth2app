# -*- coding: utf-8 -*-
from django.conf.urls import url

urlpatterns = [
    url(r'^date_joined/?$', 'mysite.apps.api.views', 'date_joined'),
    url(r'^last_login/?$', 'mysite.apps.api.views', 'last_login'),
    url(r'^email/?$', 'mysite.apps.api.views', 'email')
]
