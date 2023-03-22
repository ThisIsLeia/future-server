from functools import wraps
from voluptuous import Invalid
from flask import request
from future.exceptions import ValidationError


def dataschema(schema):
    """json schema"""

    def decorator(f):

        @wraps(f)
        def new_func(*args, **kwargs):
            try:
                kwargs.update(schema(request.json))
            except Invalid as e:
                path = '.'.join([str(x) for x in e.path])
                raise ValidationError(f"{e.msg} ({path})")
            return f(*args, **kwargs)

        return new_func

    return decorator
