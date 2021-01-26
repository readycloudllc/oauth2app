# -*- coding: utf-8 -*-
from django.conf.urls import url

urlpatterns = [
    url(r'^automatic_error_str/?$', 'testsite.apps.api.views', 'automatic_error_str'),
    url(r'^automatic_error_json/?$', 'testsite.apps.api.views', 'automatic_error_json'),
    url(r'^first_name_str/?$', 'testsite.apps.api.views', 'first_name_str'),
    url(r'^first_and_last_name_str/?$', 'testsite.apps.api.views', 'first_and_last_name_str'),
    url(r'^last_name_str/?$', 'testsite.apps.api.views', 'last_name_str'),
    url(r'^email_str/?$', 'testsite.apps.api.views', 'email_str'),
    url(r'^email_json/?$', 'testsite.apps.api.views', 'email_json')
]
