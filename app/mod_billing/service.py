from functools import wraps
from flask import request
from app.mod_common.service import BaseService
from app.mod_auth.service import Service as AuthService
from app.mod_role.service import Service as RoleService
from app.mod_account.service import Service as AccountService
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

            print(retf)

            if retf and isinstance(retf, tuple) and retf[1] in [200, 201]:
                obj = {}
                key = request.headers.get('Authorization')
                if "key" in retf[0].keys():
                    key = retf[0]["key"]
                module_name = args[0].__class__.__module__
                class_name = args[0].__class__.__name__
                method_name = function.__name__
                base_url = request.base_url
                ret = AuthService.is_role_member(
                    key, module_name,
                    class_name, method_name)

                print("RETTT", ret)

                if ret and not isinstance(ret, str):
                    account, user = ret
                    role = RoleService.read_by_attrs(
                        module_name, class_name,
                        method_name)
                    if role:
                        account_role = AccountService.read_account_role(
                            account_id=account.id, role_id=role.id)
                        if account_role:

                            print(account_role.cost)

                            obj = {"base_url": base_url,
                                   "account_role": account_role.id,
                                   "user": user.id,
                                   "cost": account_role.cost}
                            ret = cls.create(obj, serialize=False)

                            print(ret)

            return retf
        return wrapper
