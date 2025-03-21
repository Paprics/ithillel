import sys
from collections import OrderedDict
from functools import wraps


def get_size(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        size = sys.getsizeof(result)
        print(f'Size - {size} bytes.')
        return result

    return wrapper


def lfu_cache(max_limit=64):
    def cache_decorator(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))

            if cache_key in decorator._cache:
                decorator._total[cache_key] += 1
                return decorator._cache[cache_key]

            result = func(*args, **kwargs)

            if len(decorator._cache) >= max_limit:
                lfu_key = min(decorator._total, key=decorator._total.get)
                del decorator._cache[lfu_key]
                del decorator._total[lfu_key]

            decorator._cache[cache_key] = result
            decorator._total[cache_key] = 1

            return result

        decorator._cache = OrderedDict()
        decorator._total = {}
        return decorator

    return cache_decorator