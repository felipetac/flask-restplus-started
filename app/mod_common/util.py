from urllib import parse
from functools import wraps
from flask import request
from app import DB
#class method decorator
class Util(object):

    @classmethod
    def marshal_paginate(cls, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            data = function(*args, **kwargs)
            if isinstance(data, tuple):
                data = data[0]
            if isinstance(data, dict) and "page" in data.keys():
                for k in ["curr", "prev", "next", "last"]:
                    if k in data["page"].keys() and data["page"][k]:
                        data["page"][k] = parse.urljoin(request.base_url, str(data["page"][k]))
            return data
        return wrapper

    @staticmethod
    def get_class_attributes(_class):
        return [i for i in dir(_class) if not callable(i) and not i.startswith('_') and  \
                i not in ["metadata", "query", "query_class"]]

    @staticmethod
    def get_class_methods(_class):
        methods = [func for func in dir(_class) if callable(getattr(_class, func)) and \
                not func.startswith("__")]
        methods = [m for m in methods if m != "Meta"]
        return methods

    @staticmethod
    def model_exists(model_class):
        return model_class.metadata.tables[model_class.__tablename__].exists(DB.engine)
