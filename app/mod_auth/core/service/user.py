from app import DB
from app.mod_auth.core.model.user import User as UserModel, UserSchema
from app.mod_auth.core.form.user import UserForm

class User():

    @staticmethod
    def list():
        users = UserModel.query.all()
        if users:
            user_schema = UserSchema(many=True)
            return user_schema.dump(users)
        return []

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

    @staticmethod
    def read(user_id, serializer=True):
        user = UserModel.query.filter_by(id=user_id).first()
        if user:
            if serializer:
                user_schema = UserSchema()
                return user_schema.dump(user)
            return user
        return None

    @classmethod
    def update(cls, user_id, json_obj):
        user = cls.read(user_id, serializer=False)
        if user:
            form = UserForm.from_json(json_obj, obj=user) # obj to raising a ValidationError
            if form.validate_on_submit():
                form.populate_obj(user)
                DB.session.commit()
                user_schema = UserSchema()
                return user_schema.dump(user) # Return user with last id insert
            return {"form": form.errors}
        return None

    @classmethod
    def delete(cls, user_id):
        user = cls.read(user_id, serializer=False)
        if user:
            DB.session.delete(user)
            DB.session.commit()
            return True
        return None
