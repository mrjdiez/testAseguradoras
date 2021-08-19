from functools import wraps

from flask import request, make_response, abort


def to_json(item):
    if isinstance(item, (list, tuple)):
        return [to_json(element) for element in item]
    return {key: value for key, value in item.__dict__.items() if not key.startswith('_')}


def flatten(items):
    return [element for item in items for element in item]


def validate_params(*params):
    def _decorator(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            if not request.is_json:
                abort(400, "Request must be JSON encoded")
            request_body = request.get_json()
            missing_params = [param for param in params if param not in request_body]
            if missing_params:
                abort(400, f"Missing required parameters [{', '.join(missing_params)}]")
            return func(*args, **kwargs)
        return _wrapped
    return _decorator
