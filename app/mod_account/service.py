from app.mod_common.service import BaseService
from app.mod_common.util import Util
from .model import Model, Schema, AccountRole
from .form import Form


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def read_by_code(cls, code_name, serialize=True):
        if code_name and isinstance(code_name, str):
            entity = cls.Meta.model.query.filter_by(
                code_name=code_name).first()
            if entity:
                if serialize:
                    entity_schema = cls.Meta.schema()
                    return entity_schema.dump(entity)
                return entity
        return None

    @classmethod
    def get_account_role_choices(cls):
        choices = []
        model = AccountRole()
        if Util.model_exists(model):
            entities = model.query.all()
            for entity in entities:
                choices.append((entity.id, "%s | %s" %
                                (entity.account.code_name, entity.role.name)))
        return choices
    @staticmethod
    def read_account_role(prk=None, account_id=None, role_id=None):
        model = AccountRole()
        if prk and isinstance(id, int):
            entity = model.query.filter_by(id=prk).first()
            if entity:
                return entity
        elif (account_id and role_id and isinstance(account_id, int) and isinstance(role_id, int)):
            entity = model.query.filter_by(account_id=account_id, role_id=role_id).first()
            if entity:
                return entity
        return None
