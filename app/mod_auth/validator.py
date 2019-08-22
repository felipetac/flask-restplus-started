import jwt
from flask import request, current_app
from wtforms.validators import ValidationError
from app.mod_user.service import Service as UserService
from app.mod_context.service import Service as ContextService
from app.mod_contract.service import Service as ContractService


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
        if issuer and issuer.find("contrato") < 0 and issuer.find("app") < 0:
            raise ValidationError("Emissor inválido.")
        if issuer and issuer.find("contrato") != -1:
            contract = ContractService.read_by_issuer(issuer)
            if not contract:
                raise ValidationError("Contrato inválido.")
            if not contract.is_active:
                raise ValidationError("Contrato expirado.")
            if not user or issuer not in [c.issuer for c in user.contracts]:
                raise ValidationError("Contrato sem associação com o usuário.")
        if issuer and issuer.find("app") != -1:
            context = ContextService.read_by_issuer(issuer)
            if not context:
                raise ValidationError("Contexto inválido.")
            contracts_id = [c.contract.id for c in context.contexts if c.contract.is_active]
            if not contracts_id:
                raise ValidationError("Contexto não possui contratos ativos.")
            if user:
                user_contracts_ids = [c.id for c in user.contracts if c.is_active]
                if not [c for c in user_contracts_ids if c in contracts_id]:
                    raise ValidationError("Contexto sem associação com o usuário.")
            else:
                raise ValidationError("Contexto sem associação com o usuário.")
