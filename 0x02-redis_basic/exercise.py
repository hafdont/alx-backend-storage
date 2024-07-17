#!/usr/bin/env python3
"""
This module contains the Cache class which uses Redis for storing data,
retrieving data, counting method calls, storing call history, and replaying the history.
"""
import redis
import uuid
from typing import Union, Callable, Optional
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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.
    
    Args:
        method (Callable): The method to be decorated.
    
    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store the inputs and outputs of the original method.
        """
        key = method.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"

        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output)
        
        return output
    return wrapper


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

    @count_calls
    @call_history
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

    def replay(self, method: Callable):
        """
        Display the history of calls of a particular function.
        
        Args:
            method (Callable): The function to replay the history for.
        """
        key = method.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"

        inputs = self._redis.lrange(inputs_key, 0, -1)
        outputs = self._redis.lrange(outputs_key, 0, -1)

        print(f"{key} was called {len(inputs)} times:")
        for input, output in zip(inputs, outputs):
            print(f"{key}(*{input.decode('utf-8')}) -> {output.decode('utf-8')}")


if __name__ == "__main__":
    cache = Cache()

    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    cache.replay(cache.store)
