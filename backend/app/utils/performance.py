import time
import functools
import logging

def measure_performance(func):
    """Decorator to measure time of a function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info("Performance: %s executed in %.4f seconds.", func.__name__, execution_time)
        return result
    return wrapper
