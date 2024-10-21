import hashlib
import re


def shorten_url(url):
    short_hash = hashlib.md5(url.encode()).hexdigest()[:6]
    return short_hash

def is_valid_url(url):
    url_regex = re.compile(
        r'^[^\s/$.?#].[^\s]*$', re.IGNORECASE)
    return re.match(url_regex, url) is not None
