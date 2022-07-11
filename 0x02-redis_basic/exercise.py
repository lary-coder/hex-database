#!/usr/bin/env python3
"""Redis"""

from typing import Union, Callable, Optional
import redis
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper"""
        self._redis.incr(key)

        return method(self, *args, **kwds)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Method to store the history of inputs and outputs for
    a particular function
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper"""
        self._redis.rpush(inputs, str(args))
        a = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(a))

        return a

    return wrapper


def replay(method: Callable):
    """Method to display the history of calls of a particular function"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))
    inputList = redis.lrange(inputs, 0, -1)
    outputList = redis.lrange(outputs, 0, -1)
    redis_zipped = list(zip(inputList, outputList))

    for a, b in redis_zipped:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))


class Cache:
    """Class cache"""

    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store the input data in Redis using the random key
            Args:
                -data: data to be stored
            Return:
                -the random generate key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Convert the data back to the desired format
            Args:
                key: generated key
                fn:  Callable used to convert the data
            Return:
                Converted data
        """
        data = self._redis.get(key)

        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Convert data to str"""
        data = self._redis.get(key)

        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Convert data to int"""
        data = self._redis.get(key)

        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0

        return data
