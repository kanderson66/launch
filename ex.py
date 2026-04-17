from time import perf_counter
from functools import lru_cache

def time_runs(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        return_value = func(*args, **kwargs)
        print(f"The function ran in {perf_counter()-start} seconds")
        return return_value
    return wrapper

@time_runs
@lru_cache
def is_prime(n):
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True

print(is_prime(97))    # First call - runs actual computation
# The function ran in 0.0001234 seconds
# True

print(is_prime(97))    # Second call - uses cache
# The function ran in 0.0000012 seconds  # Much faster!
# True