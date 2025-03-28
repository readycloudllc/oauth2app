"""OAuth 2.0 Django Models"""
import sys
import time
from hashlib import sha512
from uuid import uuid4

from django.conf import settings
from django.db import models
from jsonfield.fields import JSONField

from .consts import (
    ACCESS_TOKEN_EXPIRATION,
    ACCESS_TOKEN_LENGTH,
    CLIENT_KEY_LENGTH,
    CLIENT_SECRET_LENGTH,
    CODE_EXPIRATION,
    CODE_KEY_LENGTH,
    MAC_KEY_LENGTH,
    REFRESHABLE,
    REFRESH_TOKEN_LENGTH,
    SCOPE_LENGTH,
)

PY3 = sys.version_info[0] == 3
AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class TimestampGenerator:
    """Callable Timestamp Generator that returns a UNIX time integer.

    **Kwargs:**

    * *seconds:* A integer indicating how many seconds in the future the
      timestamp should be. *Default 0*

    *Returns int*
    """

    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds

    def deconstruct(self):
        return ("oauth2app.oauth2app.models.TimestampGenerator", [], {})


class KeyGenerator:
    """Callable Key Generator that returns a random keystring.

    **Args:**

    * *length:* A integer indicating how long the key should be.

    *Returns str*
    """

    def __init__(self, length=16):
        self.length = length

    def __call__(self):
        return sha512(uuid4().hex.encode("utf-8")).hexdigest()[0:self.length]

    def deconstruct(self):
        kwargs = {"length": 30}
        return ("oauth2app.oauth2app.models.KeyGenerator", [], kwargs)


class Client(models.Model):
    """Stores client authentication data.

    **Args:**

    * *name:* A string representing the client name.
    * *user:* A Django User object representing the client
       owner.

    **Kwargs:**

    * *description:* A string representing the client description.
      *Default None*
    * *key:* A string representing the client key. *Default 30 character
      random string*
    * *secret:* A string representing the client secret. *Default 30 character
      random string*
    * *redirect_uris:* A json representing the list of redirect_uris.
      *Default None*

    """

    name = models.CharField(max_length=256)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    key = models.CharField(unique=True, max_length=CLIENT_KEY_LENGTH, default=KeyGenerator(CLIENT_KEY_LENGTH), db_index=True)
    secret = models.CharField(unique=True, max_length=CLIENT_SECRET_LENGTH, default=KeyGenerator(CLIENT_SECRET_LENGTH))
    redirect_uris = JSONField(null=True)
    approved = models.BooleanField(default=True)
    throttle_limit_get = models.IntegerField(null=True)
    throttle_limit_other = models.IntegerField(null=True)

    @property
    def redirect_uri(self):
        if self.redirect_uris:
            return self.redirect_uris[0]

    def __str__(self):
        return self.name


class AccessRange(models.Model):
    """Stores access range data, also known as scope.

    **Args:**

    * *key:* A string representing the access range scope. Used in access
      token requests.

    **Kwargs:**

    * *description:* A string representing the access range description.
      *Default None*

    """

    key = models.CharField(unique=True, max_length=SCOPE_LENGTH, db_index=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.key

    class Meta:
        ordering = ('id', )


class AccessToken(models.Model):
    """Stores access token data.

    **Args:**

    * *client:* A oauth2app.models.Client object
    * *user:* A Django User object

    **Kwargs:**

    * *token:* A string representing the access key token. *Default 10
      character random string*
    * *refresh_token:* A string representing the access key token. *Default 10
      character random string*
    * *mac_key:* A string representing the MAC key. *Default None*
    * *expire:* A positive integer timestamp representing the access token's
      expiration time.
    * *scope:* A list of oauth2app.models.AccessRange objects. *Default None*
    * *refreshable:* A boolean that indicates whether this access token is
      refreshable. *Default False*

    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(unique=True, max_length=ACCESS_TOKEN_LENGTH, default=KeyGenerator(ACCESS_TOKEN_LENGTH), db_index=True)
    refresh_token = models.CharField(
        unique=True, blank=True, null=True, max_length=REFRESH_TOKEN_LENGTH, default=KeyGenerator(REFRESH_TOKEN_LENGTH), db_index=True
    )
    mac_key = models.CharField(unique=True, blank=True, null=True, max_length=MAC_KEY_LENGTH, default=None)
    issue = models.PositiveIntegerField(editable=False, default=TimestampGenerator())
    expire = models.PositiveIntegerField(default=TimestampGenerator(ACCESS_TOKEN_EXPIRATION))
    scope = models.ManyToManyField(AccessRange)
    refreshable = models.BooleanField(default=REFRESHABLE)

    def __str__(self):
        return self.token


class Code(models.Model):
    """Stores authorization code data.

    **Args:**

    * *client:* A oauth2app.models.Client object
    * *user:* A Django User object

    **Kwargs:**

    * *key:* A string representing the authorization code. *Default 30
      character random string*
    * *expire:* A positive integer timestamp representing the access token's
      expiration time.
    * *redirect_uri:* A string representing the redirect_uri provided by the
      requesting client when the code was issued. *Default None*
    * *scope:* A list of oauth2app.models.AccessRange objects. *Default None*

    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(unique=True, max_length=CODE_KEY_LENGTH, default=KeyGenerator(CODE_KEY_LENGTH), db_index=True)
    issue = models.PositiveIntegerField(editable=False, default=TimestampGenerator())
    expire = models.PositiveIntegerField(default=TimestampGenerator(CODE_EXPIRATION))
    redirect_uri = models.URLField(null=True)
    scope = models.ManyToManyField(AccessRange)

    def __str__(self):
        return self.key


class MACNonce(models.Model):
    """Stores Nonce strings for use with MAC Authentication.

    **Args:**

    * *access_token:* A oauth2app.models.AccessToken object
    * *nonce:* A unique nonce string.

    """

    access_token = models.ForeignKey(AccessToken, on_delete=models.CASCADE)
    nonce = models.CharField(max_length=30, db_index=True)
