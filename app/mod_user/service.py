from app.mod_common.service import BaseService
from .model import Model, Schema
from .form import Form


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def get_by_email(cls, email, serialize=True):
        if email and isinstance(email, str):
            user = Model.query.filter_by(email=email).first()
            if user:
                if serialize:
                    user_schema = Schema()
                    return {"data": user_schema.dump(user)}
                return user
        return None

    @classmethod
    def get_by_cpfcnpj(cls, cpf_cnpj, serialize=True):
        if cpf_cnpj and isinstance(cpf_cnpj, str):
            user = Model.query.filter_by(cpf_cnpj=cpf_cnpj).first()
            if user:
                if serialize:
                    user_schema = Schema()
                    return {"data": user_schema.dump(user)}
                return user
        return None
