from app import DB
from app.mod_user.model import User as UserModel, UserSchema
from app.mod_user.form import User as UserForm
from app.mod_common.service import Base

class User(Base):

    class Meta:
        model = UserModel
        form = UserForm
        schema = UserSchema
        #order_by = "id" #caso queira mudar
        #sort = "desc" #caso queira mudar

    @staticmethod
    def create(json_obj):
        form = UserForm.from_json(json_obj)
        if form.validate_on_submit():
            user = UserModel()
            form.populate_obj(user)
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
                if form.validate_on_submit():
                    form.populate_obj(user)
                    DB.session.commit()
                    user_schema = UserSchema()
                    return user_schema.dump(user) # Return user with last id insert
                return {"form": form.errors}
        return None
