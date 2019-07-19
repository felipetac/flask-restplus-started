
from flask import request
from app.mod_service import SERVICE_COMPOSE

class Util(object):

    @staticmethod
    def get_price(function):
        def wrapper(*args, **kwargs):
            obj = {}
            SERVICE_COMPOSE.clear()
            obj["module_name"] = args[0].__class__.__module__
            obj["class_name"] = args[0].__class__.__name__
            obj["method_name"] = function.__name__
            obj["base_url"] = request.base_url
            from app.mod_auth.service import Service as AuthService #lazy load
            ret = AuthService.is_member(request.headers.get('Authorization'))
            if ret and not isinstance(ret, str):
                obj["user_id"] = ret.id
            ret = function(*args, **kwargs)
            print(SERVICE_COMPOSE)
            obj["service_weight"] = len(SERVICE_COMPOSE)
            print(obj)
            return ret
        return wrapper
