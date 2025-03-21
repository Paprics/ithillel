import sys
from functools import wraps

def get_size(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        size = sys.getsizeof(result)
        print(f'Size - {size} bytes.')
        return result

    return wrapper

