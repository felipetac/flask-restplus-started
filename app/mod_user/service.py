from app import DB
from app.mod_user.model import User as UserModel, UserSchema
from app.mod_user.form import User as UserForm
from app.mod_common.util import paginate
from app.mod_common.form import PageForm

class User():

    @classmethod
    @paginate(UserModel)
    def list(cls, page, json_obj):
        if page and isinstance(page, int):
            form = PageForm.from_json(json_obj)
            if form.validate(): #não utilizei o 'validate_on_form' pq ele não func. em GET
                per_page = form.per_page.data
                users = UserModel.query.order_by(UserModel.date_modified.desc())\
                                        .paginate(page, per_page, error_out=False).items
                if users:
                    user_schema = UserSchema(many=True)
                    return user_schema.dump(users)
                return []
            return {"form": form.errors}
        return None

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
        if user_id and isinstance(user_id, int):
            user = UserModel.query.filter_by(id=user_id).first()
            if user:
                if serializer:
                    user_schema = UserSchema()
                    return user_schema.dump(user)
                return user
        return None

    @classmethod
    def update(cls, user_id, json_obj):
        if user_id and isinstance(user_id, int):
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
        if user_id and isinstance(user_id, int):
            user = cls.read(user_id, serializer=False)
            if user:
                DB.session.delete(user)
                DB.session.commit()
                return True
        return None
