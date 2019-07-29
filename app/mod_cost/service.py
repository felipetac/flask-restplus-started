from app.mod_common.service import BaseService
from app.mod_role.model import Schema as RoleSchema
from .model import DB, Model, Schema
from .form import Form


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def cost_by_role_id(cls, role_id):
        if role_id and isinstance(role_id, int):
            return cls.Meta.model.query.filter_by(role_id=role_id).first()
        return None

    @classmethod
    def create_all(cls, roles):
        schema = RoleSchema()
        if roles and isinstance(roles, list):
            for role in roles:
                if isinstance(role, dict) and "id" in role.keys():
                    cost = cls.cost_by_role_id(role["id"])
                    if not cost:
                        cost = cls.Meta.model()
                        role = schema.load(role)
                        if role:
                            cost.role = role
                            DB.session.add(cost)
            DB.session.commit()
