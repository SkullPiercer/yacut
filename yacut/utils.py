import hashlib


def shorten_url(url):
    short_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    return f"http://127.0.0.1:5000/{short_hash}"