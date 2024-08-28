#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import Redis
import uuid


class Cache:
    """
    Create a Cache class
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, bytes, float]) -> str:
        """
        store a data argument and returns a string
        """
        uuid_num = str(uuid.uuid4())
        self._redis.set(uuid_num, data)

        return uuid_num
