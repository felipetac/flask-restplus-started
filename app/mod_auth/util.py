from functools import wraps
from flask import request, current_app
from flask_restplus import abort
import jwt
from app.mod_user.service import User as UserService
from app.mod_role.service import Role


class Auth(object):

    @classmethod
    def required(cls, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user = cls.__is_member()
            if user:
                return function(*args, **kwargs)
            abort(401, "Token inválido!", statusCode=401)
        return wrapper

    @classmethod
    def role_required(cls, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user = cls.__is_member()
            if user:
                module_name = args[0].__class__.__module__
                class_name = args[0].__class__.__name__
                method_name = function.__name__
                role = Role.read_by_attrs(module_name, class_name, method_name)
                if role and role.role_name in [role.role_name for role in user.roles]:
                    return function(*args, **kwargs)
                abort(401, "Token não possui autorização " +
                      "para efetuar esta requisição!", statusCode=401)
            abort(401, "Token inválido!", statusCode=401)
        return wrapper

    @staticmethod
    def __is_member():
        try:
            key = request.headers.get('Authorization')
            if key:
                payloads = jwt.decode(key.replace("Bearer ", ""),
                                      current_app.config["SECRET_KEY"],
                                      current_app.config["JWT_ALGORITHM"])
                user = UserService.get_by_email(payloads["email"], serializer=False)
                if user:
                    return user
                abort(401, "Token inválido!", statusCode=401)
            abort(401, "Token é requerido para esta requisição!", statusCode=401)
        except jwt.exceptions.DecodeError:
            abort(401, "Token inválido!", statusCode=401)
