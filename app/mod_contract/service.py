from app.mod_common.service import BaseService
from app.mod_user.service import Service as UserService
from app.mod_role.service import Service as RoleService
from .model import DB, Model, Schema
from .form import Form


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def create(cls, json_obj, serializer=True):
        form = Form.from_json(cls._json_obj(json_obj))
        form.users_id.choices = UserService.get_choices()
        form.roles_id.choices = RoleService.get_choices()
        if form.validate_on_submit():
            entity = cls._populate_obj(form, Model())
            DB.session.add(entity)
            DB.session.commit()
            if serializer:
                schema = Schema()
                return schema.dump(entity)  # Return user with last id insert
            return entity
        return {"form": form.errors}

    @classmethod
    def update(cls, entity_id, json_obj, serializer=True):
        if entity_id and isinstance(entity_id, int):
            entity = cls.read(entity_id, serializer=False)
            if entity:
                form = Form.from_json(cls._json_obj(json_obj),
                                      obj=entity)  # obj to raising a ValidationError
                form.users_id.choices = UserService.get_choices()
                form.roles_id.choices = RoleService.get_choices()
                if form.validate_on_submit():
                    entity = cls._populate_obj(form, entity)
                    DB.session.commit()
                    if serializer:
                        schema = Schema()
                        # Return entity with last id insert
                        return schema.dump(entity)
                    return entity
                return {"form": form.errors}
        return None

    @staticmethod
    def _json_obj(json_obj):  # Fix por causa do exemplo gerado pelo swagger
        keys = json_obj.keys()
        if "users_id" in keys and json_obj["users_id"] == [0]:
            del json_obj["users_id"]
        if "roles_id" in keys and json_obj["roles_id"] == [0]:
            del json_obj["roles_id"]
        return json_obj

    @staticmethod
    def _populate_obj(form, entity):
        form.populate_obj(entity)
        if form.users_id.data:
            for user_id in form.users_id.data:
                if user_id not in [user.id for user in entity.users]:
                    user = UserService.read(user_id, serializer=False)
                    entity.users.append(user)
        if form.roles_id.data:
            for role_id in form.roles_id.data:
                if role_id not in [role.id for role in entity.roles]:
                    role = RoleService.read(role_id, serializer=False)
                    entity.roles.append(role)
        return entity
