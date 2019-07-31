import datetime
from functools import wraps
import jwt
from flask import request, current_app
from flask_restplus import abort
from app.mod_user.service import Service as UserService
from app.mod_role.service import Service as RoleService
from app.mod_contract.service import Service as ContractService
from app.mod_auth.form import LoginForm


class Service:

    @staticmethod
    def get_key(json_obj):
        form = LoginForm.from_json(json_obj)
        if form.validate_on_submit():
            user = UserService.get_by_email(form.email.data, serialize=False)
            if user and user.password == form.password.data:
                if not ContractService.read_by_issuer(form.issuer.data):
                    return {"form": "Emissor não existe."}
                if not form.issuer.data in [c.issuer for c in user.contracts]:
                    return {"form": "Usuário não associado a este emissor."}
                delta_sec = current_app.config["JWT_EXPIRATION_SECONDS"] or 420
                dt_now = datetime.datetime.utcnow()
                payloads = {"sub": user.id, "user": user.name, "email": user.email,
                            "iss": form.issuer.data, "iat": dt_now,
                            "exp": (dt_now + datetime.timedelta(seconds=delta_sec))}
                encoded_jwt = jwt.encode(payloads, current_app.config["SECRET_KEY"],
                                         current_app.config["JWT_ALGORITHM"])
                return {"data": {"key": encoded_jwt.decode("utf-8")}}
            return {"form": "Usuário ou senha inválidos!"}
        return {"form": form.errors}

    @staticmethod
    def is_member(key):
        if key:
            try:
                payloads = jwt.decode(key.replace("Bearer ", ""),
                                      current_app.config["SECRET_KEY"],
                                      current_app.config["JWT_ALGORITHM"])
                user = UserService.get_by_email(
                    payloads["email"], serialize=False)
                if user:
                    contract = ContractService.read_by_issuer(payloads["iss"])
                    if not contract:
                        return "O emissor do token não foi encontrado!"
                    if not contract.active:
                        return "O emissor do token está inativo!"
                    if contract.id not in [c.id for c in user.contracts]:
                        return "Usuário não está associado ao emissor do token!"
                    return (contract, user)
            except jwt.ExpiredSignatureError:
                return "Token está expirado!"
            except jwt.DecodeError:
                return "Token Inválido!"
            return "Token inválido!"
        return "Token é requerido para esta requisição!"

    @classmethod
    def is_role_member(cls, key, module_name, class_name, method_name):
        ret = cls.is_member(key)
        if ret and not isinstance(ret, str):
            contract, user = ret
            roles_excluded = [r.id for r in user.roles_excluded]
            roles_ids = [r.id for r in contract.roles]
            user_roles = [r for r in roles_ids if r not in roles_excluded]
            role = RoleService.read_by_attrs(
                module_name, class_name, method_name)
            if role and role.id in user_roles:
                return (contract, user)
            return "Token não possui autorização para efetuar esta requisição!"
        return ret

    @classmethod
    def required(cls, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            module_name = args[0].__class__.__module__
            class_name = args[0].__class__.__name__
            method_name = function.__name__
            ret = cls.is_role_member(request.headers.get('Authorization'),
                                     module_name, class_name, method_name)
            if ret and not isinstance(ret, str):
                return function(*args, **kwargs)
            abort(401, ret, statusCode=401)
        return wrapper
