import hashlib
import re

from .constants import URL_LEN


def shorten_url(url):
    return hashlib.md5(url.encode()).hexdigest()[:URL_LEN]


def is_valid_url(url):
    url_regex = re.compile(r'^(?=.*[A-Za-z])[A-Za-z0-9]+$', re.IGNORECASE)
    return re.match(url_regex, url) is not None
