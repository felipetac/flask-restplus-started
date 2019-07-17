from app.mod_common.service import BaseService
from app.mod_user.service import Service as UserService
from .model import DB, Model, Schema
from .form import Form

class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def create(cls, json_obj):
        if "id" in json_obj.keys():
            del json_obj["id"]
        form = Form.from_json(json_obj)
        print(form.user_id.data, form.method_name.data)
        form.user_id.choices = UserService.get_choices()
        if form.validate():
            auth = cls._populate_obj(form, Model())
            DB.session.add(auth)
            DB.session.commit()
            schema = Schema()
            return schema.dump(auth) # Return user with last id insert
        return {"form": form.errors}

    @staticmethod
    def _populate_obj(form, auth):
        form.populate_obj(auth)
        if form.user_id.data:
            user = UserService.read(form.user_id.data, serializer=False)
            auth.user = user
        return auth
