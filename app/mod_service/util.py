from functools import wraps
from . import SERVICE_COMPOSE
from .service import Service

class Util(object):

    @staticmethod
    def compose(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            obj = {}
            obj["module_name"] = args[0].__module__
            obj["class_name"] = args[0].__name__
            obj["method_name"] = function.__name__
            ret = Service.read_by_attrs(obj["module_name"],
                                        obj["class_name"],
                                        obj["method_name"])
            if not ret:
                ret = Service.create(obj, serializer=False)
            SERVICE_COMPOSE.append(ret)
            return function(*args, **kwargs)
        return wrapper
