#!/usr/bin/env python3
"""
This module contains the get_page function which uses Redis for caching web page content.
"""
import redis
import requests
from typing import Callable
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    
    Args:
        method (Callable): The method to be decorated.
    
    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to increment the call count and call the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def get_page(url: str) -> str:
    """
    Get the HTML content of a URL and cache the result in Redis with an expiration time of 10 seconds.
    
    Args:
        url (str): The URL to get the content for.
    
    Returns:
        str: The HTML content of the URL.
    """
    _redis = redis.Redis()
    count_key = f"count:{url}"
    _redis.incr(count_key)

    cached_content = _redis.get(url)
    if cached_content:
        return cached_content.decode("utf-8")

    response = requests.get(url)
    _redis.setex(url, 10, response.text)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))
