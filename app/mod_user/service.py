from app.mod_common.service import DB, BaseService
from app.mod_role.service import Service as RoleService
from .model import Model, Schema
from .form import Form

class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema
        #order_by = "id" #caso queira mudar
        #sort = "desc" #caso queira mudar

    @classmethod
    def create(cls, json_obj, serializer=True):
        if "id" in json_obj.keys():
            del json_obj["id"]
        form = Form.from_json(json_obj)
        form.roles_id.choices = RoleService.get_choices()
        if form.validate_on_submit():
            user = cls._populate_obj(form, Model())
            DB.session.add(user)
            DB.session.commit()
            if serializer:
                user_schema = Schema()
                return user_schema.dump(user) # Return user with last id insert
            return user
        return {"form": form.errors}

    @classmethod
    def update(cls, entity_id, json_obj, serializer=True):
        if "id" in json_obj.keys():
            del json_obj["id"]
        if entity_id and isinstance(entity_id, int):
            user = cls.read(entity_id, serializer=False)
            if user:
                form = Form.from_json(json_obj, obj=user) # obj to raising a ValidationError
                form.roles_id.choices = RoleService.get_choices()
                if form.validate_on_submit():
                    user = cls._populate_obj(form, user)
                    DB.session.commit()
                    if serializer:
                        user_schema = Schema()
                        return user_schema.dump(user) # Return user with last id insert
                    return user
                return {"form": form.errors}
        return None

    @classmethod
    def get_choices(cls):
        user = Model.query.all()
        return [(u.id, u.name) for u in user]

    @classmethod
    def get_by_email(cls, email, serializer=True):
        if email and isinstance(email, str):
            user = Model.query.filter_by(email=email).first()
            if user:
                if serializer:
                    user_schema = Schema()
                    return {"data": user_schema.dump(user)}
                return user
        return None

    @staticmethod
    def _populate_obj(form, user):
        form.populate_obj(user)
        if form.roles_id.data:
            for role_id in form.roles_id.data:
                if role_id not in [role.id for role in user.roles]:
                    role = RoleService.read(role_id, serializer=False)
                    user.roles.append(role)
        return user
