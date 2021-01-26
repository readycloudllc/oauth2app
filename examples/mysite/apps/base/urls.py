# -*- coding: utf-8 -*-
from django.conf.urls import url

urlpatterns = [
    url(r'^/?$', 'mysite.apps.base.views', 'homepage'),
]
