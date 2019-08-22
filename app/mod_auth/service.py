import datetime
from functools import wraps
import jwt
from flask import request, current_app
from flask_restplus import abort
from app.mod_user.service import Service as UserService
from app.mod_role.service import Service as RoleService
from app.mod_contract.service import Service as ContractService
from app.mod_contract.service import Model as Contract
from app.mod_context.service import Service as ContextService
from app.mod_context.model import Model as Context
from app.mod_auth.form import LoginForm, KeyForm
from .validator import Key as KeyValidator


class Service:

    @staticmethod
    def get_issuer_key_exp(issuer):
        key_exp = current_app.config["JWT_EXPIRATION_SECONDS"] or 420
        if issuer:
            if issuer.find("contract") != -1:
                contract = ContractService.read_by_issuer(issuer)
                key_exp = contract.key_exp if contract.key_exp else key_exp
            if issuer.find("app") != -1:
                context = ContextService.read_by_issuer(issuer)
                key_exp = context.key_exp if context.key_exp else key_exp
        return key_exp

    @classmethod
    def get_key(cls, json_obj):
        form = LoginForm.from_json(json_obj)
        if form.validate_on_submit():
            user = UserService.get_by_email(form.email.data, serialize=False)
            issuer = form.issuer.data or None
            delta_sec = cls.get_issuer_key_exp(issuer)
            dt_now = datetime.datetime.utcnow()
            payloads = {"ip": request.remote_addr, "sub": user.id, "user": user.name,
                        "email": user.email, "iss": form.issuer.data, "iat": dt_now,
                        "exp": (dt_now + datetime.timedelta(seconds=delta_sec))}
            encoded_jwt = jwt.encode(payloads, current_app.config["SECRET_KEY"],
                                     current_app.config["JWT_ALGORITHM"])
            return {"key": encoded_jwt.decode("utf-8"), "expiration": payloads["exp"]}
        return {"form": form.errors}

    @classmethod
    def refresh_key(cls, json_obj):
        form = KeyForm.from_json(json_obj)
        if form.validate_on_submit():
            payloads = jwt.decode(form.key.data.replace("Bearer ", ""),
                                  current_app.config["SECRET_KEY"],
                                  current_app.config["JWT_ALGORITHM"])
            if form.issuer.data:
                payloads["iss"] = form.issuer.data
            payloads["iat"] = datetime.datetime.utcnow()
            delta_sec = cls.get_issuer_key_exp(payloads["iss"])
            payloads["exp"] = payloads["iat"] + datetime.timedelta(seconds=delta_sec)
            encoded_jwt = jwt.encode(payloads, current_app.config["SECRET_KEY"],
                                     current_app.config["JWT_ALGORITHM"])
            return {"key": encoded_jwt.decode("utf-8"), "expiration": payloads["exp"]}
        return {"form": form.errors}

    @classmethod
    def is_member(cls, key):
        if key:
            result = KeyValidator.validate(key)
            if not result:
                payloads = result
                user = UserService.get_by_email(
                    payloads["email"], serialize=False)
                if user:
                    issuer = payloads["iss"]
                    if issuer and issuer.find("contract") != -1:
                        contract = ContractService.read_by_issuer(issuer)
                        if not contract:
                            return "Contrato não encontrado."
                        if not contract.active:
                            return "Contrato está inativo."
                        if contract.id not in [c.id for c in user.contracts]:
                            return "Usuário não está associado ao contrato."
                        return (contract, user)
                    elif issuer and issuer.find("app") != -1:
                        context = ContextService.read_by_issuer(issuer)
                        if not context:
                            return "Contexto da Aplicação não encontrado."
                        return (context, user)
                return "Token Inválido!"
            return result
        return "Token é requerido para esta requisição!"

    @classmethod
    def is_role_member(cls, key, module_name, class_name, method_name):
        ret = cls.is_member(key)
        if ret and not isinstance(ret, str):
            issuer, user = ret
            roles_excluded = [r.id for r in user.roles_excluded]
            if isinstance(issuer, Contract):
                roles_ids = [r.id for r in issuer.roles]
            if isinstance(issuer, Context):
                contract_roles_id = []
                c_roles_ids = [c.role.id for c in issuer.contexts]
                c_contracts_ids = [c.contract.id for c in issuer.contexts]
                for c_id in c_contracts_ids:
                    contract = ContractService.read(c_id)
                    contract_roles_id += [r.id for r in contract.roles]
                roles_ids = [r for r in c_roles_ids if r in contract_roles_id]
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
