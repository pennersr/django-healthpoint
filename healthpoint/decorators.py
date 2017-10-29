from functools import wraps

from healthpoint.registry import register_health_check


def health_check(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isinstance(result, bool):
                success, detail = result, 'OK' if result else 'ERROR'
            elif isinstance(result, tuple) and len(result) == 2:
                success, detail = result
            else:
                raise ValueError(
                    'Your @health_check must return'
                    ' a `bool`, or a tuple of (`bool`, `detail`)')
        except Exception as e:
            success, detail = False, str(e)
        return success, detail

    register_health_check(wrapper)
    return wrapper
