from functools import wraps
from flask import request
from app.mod_common.service import BaseService
from app.mod_auth.service import Service as AuthService
from .model import Model, Schema
from .form import Form


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def register(cls, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            retf = function(*args, **kwargs)

            if isinstance(retf, list) and "key" in retf[0].keys():
                print("KEYYYY ==> ", retf[0]["key"])

            obj = {}
            obj["module_name"] = args[0].__class__.__module__
            obj["class_name"] = args[0].__class__.__name__
            obj["method_name"] = function.__name__
            obj["base_url"] = request.base_url
            ret = AuthService.is_member(request.headers.get('Authorization'))
            if ret and not isinstance(ret, str):
                _, user = ret
                obj["user_id"] = user.id
            cls.create(obj)
            return retf
        return wrapper
