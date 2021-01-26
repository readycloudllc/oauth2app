# -*- coding: utf-8 -*-
from django.conf.urls import url

urlpatterns = [
    url(r'^missing_redirect_uri/?$', 'mysite.apps.oauth2.views.missing_redirect_uri'),
    url(r'^authorize/?$', 'mysite.apps.oauth2.views.authorize'),
    url(r'^token/?$', 'oauth2app.token.handler'),
]
