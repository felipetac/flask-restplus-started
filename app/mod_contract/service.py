from app.mod_common.service import BaseService
from app.mod_common.util import Util
from .model import Model, Schema, ContractRole, ContractRoleSchema
from .form import Form


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def read_by_issuer(cls, issuer):
        model = cls.Meta.model
        res = model.query.filter(
            model.issuer == issuer).first()
        return res

    @staticmethod
    def read_contract_role(entity_id, serialize=True):
        if entity_id and isinstance(entity_id, int):
            model = ContractRole()
            entity = model.query.filter_by(
                id=entity_id).first()
            if entity:
                if serialize:
                    entity_schema = ContractRoleSchema()
                    return entity_schema.dump(entity)
                return entity
        return None

    @classmethod
    def get_contract_role_choices(cls):
        choices = []
        model = ContractRole()
        if Util.model_exists(model):
            res = model.query.all()
            if res:
                for entity in res:
                    entity = cls.read_contract_role(entity.id, serialize=False)
                    choices.append((entity.id, "%s - %s" % (entity.role.name,
                                                            entity.contract.name)))
        return choices
