from functools import wraps
import time
from ratelimit import limits, sleep_and_retry
import requests


def logger(function):
    """
    Logging when a function starts and ends executing.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"----- {function.__name__}: start -----")
        output = function(*args, **kwargs)
        print(f"----- {function.__name__}: end -----")
        return output

    return wrapper


def cache(function):
    """
    This is a built-in decorator that you can import from functools.

    It caches the return values of a function, using a least-recently-used (LRU)
    algorithm to discard the least-used values when the cache is full.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key in wrapper.cache:
            output = wrapper.cache[cache_key]
        else:
            output = function(*args)
            wrapper.cache[cache_key] = output
        return output

    wrapper.cache = dict()
    return wrapper


def repeat(number_of_times: int):
    """
    Causes a function to be called multiple times in a row.

    Parameters
    ----------
    number_of_times : int
        Repetitions
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(number_of_times):
                func(*args, **kwargs)

        return wrapper

    return decorate


def timeit(func):
    """
    timeit measures the execution time of a function and prints the result.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f} seconds to complete")
        return result

    return wrapper


def retry(num_retries: int, exception_to_check, sleep_time=0):
    """
    Decorator that retries the execution of a function if it raises a specific exception.

    Parameters
    ----------
    num_retries : int
        Number of retries
    exception_to_check : Error
        Specific exception
    sleep_time : int, optional
        Time to wait until retry, by default 0
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, num_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    print(f"{func.__name__} raised {e.__class__.__name__}. Retrying...")
                    if i < num_retries:
                        time.sleep(sleep_time)
            # Raise the exception if the function was not successful after the specified number of retries
            raise e

        return wrapper

    return decorate


def countcall(func):
    """
    Counts the number of times a function has been called.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        result = func(*args, **kwargs)
        print(f"{func.__name__} has been called {wrapper.count} times")
        return result

    wrapper.count = 0
    return wrapper


FIFTEEN_MINUTES = 900


@sleep_and_retry
@limits(calls=15, period=FIFTEEN_MINUTES)
def call_api(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("API response: {}".format(response.status_code))
    return response
