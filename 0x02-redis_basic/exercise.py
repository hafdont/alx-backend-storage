#!/usr/bin/env python3
"""
This module contains the Cache class which uses Redis for storing data and retrieving data.
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """
    Cache class for storing data in Redis and retrieving it.
    """
    def __init__(self):
        """
        Initialize the Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key and return the key.
        
        Args:
            data (Union[str, bytes, int, float]): The data to store.
        
        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis and optionally convert it using a callable.
        
        Args:
            key (str): The key to retrieve data for.
            fn (Optional[Callable]): A callable to convert the data.
        
        Returns:
            Union[str, bytes, int, float]: The retrieved data.
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve data as a UTF-8 string.
        
        Args:
            key (str): The key to retrieve data for.
        
        Returns:
            str: The retrieved data as a string.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve data as an integer.
        
        Args:
            key (str): The key to retrieve data for.
        
        Returns:
            int: The retrieved data as an integer.
        """
        return self.get(key, int)


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
