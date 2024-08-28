#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
from uuid import uuid4
from typing import Any, Union, Optional, Callable
from functools import wraps


class Cache:
    """
    Create a Cache class
    """

    def __init__(self):
        """
        Initialize new cache object
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, bytes, float]) -> str:
        """
        store a data argument and returns a string
        """
        uuid_num = str(uuid4())
        client = self._redis
        client.set(uuid_num, data)

        return uuid_num

    def get(self, key, fn: Optional[Callable] = None):
        """
        create a get method that take a key string argument
        """
        exists = self._redis.get(key)

        if exists is None:
            return None

        if fn:
            return str(fn(exists))

        return exists

    def get_str(self, key):
        """
        get_str, get_int
        """
        return self._redis.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key):
        """
        get_str, get_int
        """
        return self._redis.get(key, fn=int)
