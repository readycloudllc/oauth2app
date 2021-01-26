# -*- coding: utf-8 -*-
from django.conf.urls import url
from oauth2app.token import TokenGenerator
from oauth2app.consts import MAC

urlpatterns = [
    url(r'^missing_redirect_uri/?$', 'testsite.apps.oauth2.views.missing_redirect_uri'),
    url(r'^authorize_not_refreshable/?$', 'testsite.apps.oauth2.views.authorize_not_refreshable'),
    url(r'^authorize_mac/?$', 'testsite.apps.oauth2.views.authorize_mac'),
    url(r'^authorize_first_name/?$', 'testsite.apps.oauth2.views.authorize_first_name'),
    url(r'^authorize_first_name/?$', 'testsite.apps.oauth2.views.authorize_last_name'),
    url(r'^authorize_first_and_last_name/?$', 'testsite.apps.oauth2.views.authorize_first_and_last_name'),
    url(r'^authorize_no_scope/?$', 'testsite.apps.oauth2.views.authorize_no_scope'),
    url(r'^authorize_code/?$', 'testsite.apps.oauth2.views.authorize_code'),
    url(r'^authorize_token/?$', 'testsite.apps.oauth2.views.authorize_token'),
    url(r'^authorize_token_mac/?$', 'testsite.apps.oauth2.views.authorize_token_mac'),
    url(r'^authorize_code_and_token/?$', 'testsite.apps.oauth2.views.authorize_code_and_token'),
    url(r'^token/?$', 'oauth2app.token.handler'),
    url(r'^token_mac/?$', TokenGenerator(authentication_method=MAC))
]
