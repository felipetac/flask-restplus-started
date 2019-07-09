from app import DB
from app.mod_user.model import User as UserModel, UserSchema
from app.mod_user.form import User as UserForm
from app.mod_common.service import Base
from app.mod_role.service import Role as RoleService

class User(Base):

    class Meta:
        model = UserModel
        form = UserForm
        schema = UserSchema
        #order_by = "id" #caso queira mudar
        #sort = "desc" #caso queira mudar

    @classmethod
    def create(cls, json_obj):
        form = UserForm.from_json(json_obj)
        form.roles_id.choices = RoleService.get_choices()
        if form.validate_on_submit():
            user = cls._populate_obj(form, UserModel())
            DB.session.add(user)
            DB.session.commit()
            user_schema = UserSchema()
            return user_schema.dump(user) # Return user with last id insert
        return {"form": form.errors}

    @classmethod
    def update(cls, entity_id, json_obj):
        if entity_id and isinstance(entity_id, int):
            user = cls.read(entity_id, serializer=False)
            if user:
                form = UserForm.from_json(json_obj, obj=user) # obj to raising a ValidationError
                form.roles_id.choices = RoleService.get_choices()
                if form.validate_on_submit():
                    user = cls._populate_obj(form, user)
                    DB.session.commit()
                    user_schema = UserSchema()
                    return user_schema.dump(user) # Return user with last id insert
                return {"form": form.errors}
        return None

    @classmethod
    def _populate_obj(cls, form, user):
        form.populate_obj(user)
        if form.roles_id.data:
            for role_id in form.roles_id.data:
                if role_id not in [role.id for role in user.roles]:
                    role = cls.read(role_id, serializer=False)
                    user.roles.append(role)
        return user
