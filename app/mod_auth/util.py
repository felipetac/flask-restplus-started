from functools import wraps
from flask import request
from flask_restplus import abort
from .service import Service


class Util(object):

    @classmethod
    def required(cls, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            ret = Service.is_member(request.headers.get('Authorization'))
            if ret and not isinstance(ret, str):
                return function(*args, **kwargs)
            abort(401, ret, statusCode=401)
        return wrapper

    @classmethod
    def role_required(cls, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            module_name = args[0].__class__.__module__
            class_name = args[0].__class__.__name__
            method_name = function.__name__
            ret = Service.is_role_member(request.headers.get('Authorization'),
                                         module_name, class_name, method_name)
            if ret and not isinstance(ret, str):
                return function(*args, **kwargs)
            abort(401, ret, statusCode=401)
        return wrapper
