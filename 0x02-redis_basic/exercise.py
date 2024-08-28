#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
from uuid import uuid4
from typing import Any, Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts method calls and increments a Redis counter"""

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapperfunction"""

        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wwrapper


def replay(method: Callable) -> str:
    """replay function"""

    m_key = method.__qualname__
    inputs = method.__qualname__ + ":inputs"
    outputs = method.__qualname__ + ":outputs"

    redis = method.__self__._redis
    print(redis)
    count = redis.get(m_key).decode("utf-8")
    print('{} was called {} times'.format(m_key, count))
    allinput = redis.lrange(inputs, 0, -1)
    alloutput = redis.lrange(outputs, 0, -1)
    allData = list(zip(alloutput, allinput))
    for k, v in allData:
        key = k.decode("utf-8")
        v = v.decode("utf-8")
        print(f"{m_key}(*{v}) -> {key}")


def call_history(method: Callable) -> Callable:
    """Get the current inputs and outputs"""
    key = method.__qualname__
    inputs = method.__qualname__ + ":inputs"
    outputs = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Callable:
        """Get the current inputs and outputs"""

        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, data)
        return data
    return wrapper


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
