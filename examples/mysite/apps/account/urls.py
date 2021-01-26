# -*- coding: utf-8 -*-
from django.conf.urls import url

urlpatterns = [
    url(r'^login/?$', 'mysite.apps.account.views', 'login'),
    url(r'^logout/?$', 'mysite.apps.account.views', 'logout'),
    url(r'^signup/?$', 'mysite.apps.account.views', 'signup'),
    url(r'^clients/?$', 'mysite.apps.account.views', 'clients'),
]
