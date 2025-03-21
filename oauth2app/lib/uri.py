# -*- coding: utf-8 -*-


"""OAuth 2.0 URI Helper Functions"""

from future.moves.urllib.parse import urlparse, urlunparse, urlencode, parse_qsl
from oauth2app.oauth2app.lib.url_normalize import url_normalize


def add_parameters(url, parameters):
    """Parses URL and appends parameters.

    **Args:**

    * *url:* URL string.
    * *parameters:* Dict of parameters

    *Returns str*"""
    parts = list(urlparse(url))
    parts[4] = urlencode(parse_qsl(parts[4]) + list(parameters.items()))
    return urlunparse(parts)


def add_fragments(url, fragments):
    """Parses URL and appends fragments.

    **Args:**

    * *url:* URL string.
    * *fragments:* Dict of fragments

    *Returns str*"""
    parts = list(urlparse(url))
    parts[5] = urlencode(parse_qsl(parts[5]) + list(fragments.items()))
    return urlunparse(parts)


def normalize(url):
    """Normalizes URL.

    **Args:**

    * *url:* URL string.

    *Returns str*"""
    return url_normalize(url)
