from app.mod_common.service import DB, Base
from .model import Role as RoleModel, RoleSchema
from .form import Role as RoleForm

class Role(Base):

    class Meta:
        model = RoleModel
        form = RoleForm
        schema = RoleSchema
        #order_by = "id" #caso queira mudar
        #sort = "desc" #caso queira mudar

    @staticmethod
    def create(json_obj):
        form = RoleForm.from_json(json_obj)
        if form.validate():
            role = RoleModel()
            form.populate_obj(role)
            DB.session.add(role)
            DB.session.commit()
            role_schema = RoleSchema()
            return role_schema.dump(role) # Return role with last id insert
        return {"form": form.errors}

    @classmethod
    def update(cls, entity_id, json_obj):
        if entity_id and isinstance(entity_id, int):
            role = cls.read(entity_id, serializer=False)
            if role:
                form = RoleForm.from_json(json_obj, obj=role) # obj to raising a ValidationError
                if form.validate_on_submit():
                    form.populate_obj(role)
                    DB.session.commit()
                    role_schema = RoleSchema()
                    return role_schema.dump(role) # Return role with last id insert
                return {"form": form.errors}
        return None

    @staticmethod
    def read_by_attrs(module_name, class_name, method_name):
        res = DB.session.query(RoleModel).filter(RoleModel.module_name == module_name,
                                                 RoleModel.class_name == class_name,
                                                 RoleModel.method_name == method_name).first()
        return res

    @classmethod
    def get_choices(cls):
        ret = cls.list()
        roles = ret["data"] if "data" in ret else []
        return [(r["id"], r["role_name"]) for r in roles]
