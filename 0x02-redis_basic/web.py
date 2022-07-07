#!/usr/bin/env python3

"""
method that implements an expiring web cache and tracker
"""

from typing import Callable
from functools import wraps
import redis
import requests


def requests_counter(method: Callable) -> Callable:
    """ Counts how many times a request has been made
    """
    r = redis.Redis()

    @wraps(method)
    def wrapper(url):
        """ wrapper fxn that counts actual no of requests made"""
        cacheKey = "cached:" + url
        countKey = "count:" + url

        r.incr(countKey)
        cached = r.get(cacheKey)
        if cached:
            return cached.decode('utf-8')
        html = method(url)
        r.set(cacheKey, html)
        r.expire(cacheKey, 10)
        return html

    return wrapper


@requests_counter
def get_page(url: str) -> str:
    """ obtains html content for a given site url and returns it.
    """
    resp = requests.get(url)
    return resp.text
