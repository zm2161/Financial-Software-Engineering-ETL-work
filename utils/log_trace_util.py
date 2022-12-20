import functools
import logging


def log_trace_decorator(func, count =[0]):
    """
    Wrapper decorator
    :param func: function; decorate function in logging file with indentation
    :return: function result
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        count[0] += 1
        indent = count[0] * "    "
        logging.info(f'{indent}Entering {func.__name__}')
        value = func(*args,  **kwargs)
        logging.info(f'{indent}Leaving {func.__name__}')
        count[0] -= 1
        return value
    return wrapper

