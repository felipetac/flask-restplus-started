from functools import wraps
from flask import request
from app.mod_auth.service import Service as AuthService
from .service import Service

class Util:

    @classmethod
    def register(cls, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            obj = {}
            obj["module_name"] = args[0].__class__.__module__
            obj["class_name"] = args[0].__class__.__name__
            obj["method_name"] = function.__name__
            obj["base_url"] = request.base_url
            ret = AuthService.is_member(request.headers.get('Authorization'))
            if ret and not isinstance(ret, str):
                obj["user_id"] = ret.id
            Service.create(obj)
            return function(*args, **kwargs)
        return wrapper
