import datetime
import jwt
from flask import current_app
from app.mod_user.service import Service as UserService
from app.mod_role.service import Service as RoleService
from app.mod_auth.form import LoginForm

class Service:

    @staticmethod
    def get_key(json_obj):
        form = LoginForm.from_json(json_obj)
        if form.validate_on_submit():
            user = UserService.get_by_email(form.email.data, serializer=False)
            if user and user.password == form.password.data:
                delta_sec = current_app.config["JWT_EXPIRATION_SECONDS"] or 420
                payloads = {"user": user.name, "email": user.email,
                            "exp": (datetime.datetime.utcnow() +
                                    datetime.timedelta(seconds=delta_sec))}
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
                user = UserService.get_by_email(payloads["email"], serializer=False)
                if user:
                    return user
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
            user = ret
            role = RoleService.read_by_attrs(module_name, class_name, method_name)
            if role and role.role_name in [role.role_name for role in user.roles]:
                return user
            return "Token não possui autorização para efetuar esta requisição!"
        return ret