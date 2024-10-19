import hashlib
import re


def shorten_url(url):
    short_hash = hashlib.md5(url.encode()).hexdigest()[:6]
    return f"http://127.0.0.1:5000/{short_hash}"

def is_valid_url(url):
    url_regex = re.compile(
        r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.IGNORECASE)
    return re.match(url_regex, url) is not None
