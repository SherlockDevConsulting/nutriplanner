import time
import functools
import logging

def measure_performance(func):
    """Décorateur pour mesurer les performances d'une fonction."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Performance: {func.__name__} exécutée en {execution_time:.4f} secondes.")
        return result
    return wrapper
