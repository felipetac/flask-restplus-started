from functools import wraps
from flask import request
from app.mod_common.service import BaseService
from app.mod_auth.service import Service as AuthService
from app.mod_role.service import Service as RoleService
from app.mod_cost.service import Service as CostService
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
            obj = {}
            key = request.headers.get('Authorization')
            module_name = args[0].__class__.__module__
            class_name = args[0].__class__.__name__
            method_name = function.__name__
            base_url = request.base_url
            ret = AuthService.is_role_member(
                key, module_name,
                class_name, method_name)
            if ret and not isinstance(ret, str):
                cost = None
                contract, user = ret
                role = RoleService.read_by_attrs(
                    module_name, class_name,
                    method_name)
                if role:
                    cost = CostService.read_by_role(role.id)
                if cost:
                    obj = {"base_url": base_url,
                           "contract_id": contract.id,
                           "user_id": user.id,
                           "cost_id": cost.id}
                    cls.create(obj, serialize=False)
                return function(*args, **kwargs)
        return wrapper
