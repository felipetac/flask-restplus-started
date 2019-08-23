import jwt
from flask import request, current_app
from wtforms.validators import ValidationError
from app.mod_user.service import Service as UserService
from app.mod_account.service import Service as AccountService


class Key(object):

    def __call__(self, form, field):
        try:
            payloads = jwt.decode(field.data.replace("Bearer ", ""),
                                  current_app.config["SECRET_KEY"],
                                  current_app.config["JWT_ALGORITHM"])
            if not payloads["ip"] or payloads["ip"] != request.remote_addr:
                raise ValidationError("IP do cliente não reflete o da chave.")
            return payloads
        except jwt.ExpiredSignatureError:
            raise ValidationError("Chave expirada.")
        except jwt.DecodeError:
            raise ValidationError("Chave inválida.")

class Password(object):
    def __init__(self, message=None):
        if not message:
            message = "Senha inválida."
        self.message = message

    def __call__(self, form, field):
        user = UserService.get_by_email(form.email.data, serialize=False)
        if not user or user.password != field.data:
            raise ValidationError(self.message)

class EmailExists(object):

    def __init__(self, message=None):
        if not message:
            message = "Email não cadastrado no sistema."
        self.message = message

    def __call__(self, form, field):
        user = UserService.get_by_email(field.data, serialize=False)
        if not user:
            raise ValidationError(self.message)

class Issuer(object):

    def __call__(self, form, field):
        issuer = field.data
        user = None
        if "email" in dir(form) and form.email.data:
            user = UserService.get_by_email(form.email.data, serialize=False)
        if "key" in dir(form) and form.key.data:
            payloads = jwt.decode(form.key.data.replace("Bearer ", ""),
                                  current_app.config["SECRET_KEY"],
                                  current_app.config["JWT_ALGORITHM"])
            if payloads:
                user = UserService.get_by_email(payloads["email"], serialize=False)
        if issuer:
            account = AccountService.read_by_code(issuer, serialize=False)
            if not account:
                raise ValidationError("Emissor do token inválido.")
            if account and not account.is_active:
                raise ValidationError("Emissor do token expirado.")
            if not user or issuer not in [c.code_name for c in user.accounts]:
                raise ValidationError("Emissor do token sem associação com o usuário.")
