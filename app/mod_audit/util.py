from functools import wraps
from flask import request
from app.mod_auth.util import Util as AUTH
from .form import Form
from .model import DB, Model

class Util:

    @classmethod
    def register(cls, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            ret, obj = function(*args, **kwargs), {}
            obj["module_name"] = args[0].__class__.__module__
            obj["class_name"] = args[0].__class__.__name__
            obj["method_name"] = function.__name__
            obj["base_url"] = request.base_url
            form = Form.from_json(obj)
            if form.validate():
                model = Model()
                form.populate_obj(model)
                member = AUTH.is_member()
                if member and not isinstance(member, str):
                    model.user = member
                DB.session.add(model)
                DB.session.commit()
            return ret
        return wrapper
