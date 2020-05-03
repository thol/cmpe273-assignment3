import pickle
import hashlib
from lru_cache import lru_cache_obj
import functools


def lru_cache(cache_size):
    def lru_cache_decorator(func):
        @functools.wraps(func)
        def wrapper_lru_cache(*args, **kwargs):
            cache_obj = lru_cache_obj(cache_size)
            # print("********"+func.__name__+"********")
            if func.__name__ == "serialize_PUT":
                key, value = func(*args, **kwargs)
                cache_obj.set(key, value)
                return key, value
            if func.__name__ == "serialize_GET":
                key = args
                value = cache_obj.get(*args)
                if (value == -1):
                    key, value = func(*args, **kwargs)
                return key, value
            if func.__name__ == "serialize_DELETE":
                key = args
                value = cache_obj.delete(*args)
                if (value == -1):
                    key, value = func(*args, **kwargs)
                return key, value
        return wrapper_lru_cache
    return lru_cache_decorator

def serialize(object):
    return pickle.dumps(object)


def deserialize(object_bytes):
    return pickle.loads(object_bytes)


def hash_code_hex(data_bytes):
    hash_code = hashlib.md5(data_bytes)
    return hash_code.hexdigest()


@lru_cache(5)
def serialize_PUT(object):
    object_bytes = pickle.dumps(object)
    hash_code = hash_code_hex(object_bytes)
    envelope_bytes = pickle.dumps({
        'operation': 'PUT',
        'id': hash_code,
        'payload': object
    })
    return envelope_bytes, hash_code

@lru_cache(5)
def serialize_GET(id):
    envelope_bytes = pickle.dumps({
        'operation': 'GET',
        'id': id
    })
    return envelope_bytes, id

@lru_cache(5)
def serialize_DELETE(id):
    envelope_bytes = pickle.dumps({
        'operation': 'DELETE',
        'id': id
    })
    return envelope_bytes, id


def test():
    data_bytes, hash_code = serialize_PUT({ 'user': 'Foo' })
    print(f"Data Bytes={data_bytes}\nHash Code={hash_code}")

