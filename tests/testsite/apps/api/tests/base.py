# -*- coding: utf-8 -*-

try:
    import simplejson as json
except ImportError:
    import json
try:
    from django.contrib.auth import get_user_model  # Django 1.5+
except ImportError:
    from django.contrib.auth.models import User
from oauth2app.models import Client
from django.test.client import Client as DjangoTestClient
from django.utils import unittest
from base64 import b64encode
from future.moves.urllib.parse import urlparse, urlencode, parse_qs

USER_USERNAME = "testuser"
USER_PASSWORD = "testpassword"
USER_EMAIL = "user@example.com"
USER_FIRSTNAME = "Foo"
USER_LASTNAME = "Bar"
CLIENT_USERNAME = "client"
CLIENT_EMAIL = "client@example.com"
REDIRECT_URI = "http://example.com/callback"


class BaseTestCase(unittest.TestCase):
    user = None
    client_holder = None
    client_application = None

    def setUp(self):
        self.user = (get_user_model() or User).objects.create_user(
            USER_USERNAME,
            USER_EMAIL,
            USER_PASSWORD)
        self.user.first_name = USER_FIRSTNAME
        self.user.last_name = USER_LASTNAME
        self.user.save()
        self.client = (get_user_model() or User).objects.create_user(CLIENT_USERNAME, CLIENT_EMAIL)
        self.client_application = Client.objects.create(
            name="TestApplication",
            user=self.client)

    def tearDown(self):
        self.user.delete()
        self.client.delete()
        self.client_application.delete()

    def get_token(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)
        parameters = {
            "client_id": self.client_application.key,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code"}
        response = user.get("/oauth2/authorize_no_scope?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        code = qs['code']
        client = DjangoTestClient()
        parameters = {
            "client_id": self.client_application.key,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI}
        basic_auth = b64encode("%s:%s" % (self.client_application.key, self.client_application.secret))
        response = client.get(
            "/oauth2/token",
            parameters,
            HTTP_AUTHORIZATION="Basic %s" % basic_auth)
        return json.loads(response.content)["access_token"]
