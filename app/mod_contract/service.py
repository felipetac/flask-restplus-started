from app.mod_common.service import BaseService
from app.mod_user.service import Service as UserService
from .model import DB, Model, Schema, CONTRACT_USER
from .form import Form

class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def create(cls, json_obj, serializer=True):
        form = Form.from_json(cls._json_obj(json_obj))
        form.users_id.choices = cls._get_users()
        if form.validate_on_submit():
            entity = cls._populate_obj(form, Model())
            DB.session.add(entity)
            DB.session.commit()
            if serializer:
                schema = Schema()
                return schema.dump(entity) # Return user with last id insert
            return entity
        return {"form": cls._change_error_msg(form.errors)}

    @classmethod
    def update(cls, entity_id, json_obj, serializer=True):
        if entity_id and isinstance(entity_id, int):
            entity = cls.read(entity_id, serializer=False)
            if entity:
                form = Form.from_json(cls._json_obj(json_obj), obj=entity) # obj to raising a ValidationError
                form.users_id.choices = cls._get_users()
                if form.validate_on_submit():
                    entity = cls._populate_obj(form, entity)
                    DB.session.commit()
                    if serializer:
                        schema = Schema()
                        return schema.dump(entity) # Return entity with last id insert
                    return entity
                return {"form": cls._change_error_msg(form.errors)}
        return None

    @classmethod
    def _get_users(cls):
        choices = []
        user_choices = UserService.get_choices()
        contracts_users_ids = DB.session.query(CONTRACT_USER)\
                                        .with_entities(CONTRACT_USER.c.user_id).all()
        contracts_users_ids = [u[0] for u in contracts_users_ids]
        users_ids = [u[0] for u in user_choices]
        choices_ids = set(users_ids) - set(contracts_users_ids)
        for _id in choices_ids:
            for tpl in user_choices:
                if _id == tpl[0]:
                    choices.append(tpl)
        return choices

    @staticmethod
    def _json_obj(json_obj): # Fix por causa do exemplo gerado pelo swagger
        keys = json_obj.keys()
        if "users_id" in keys and json_obj["users_id"] == [0]:
            del json_obj["users_id"]
        return json_obj

    @staticmethod
    def _change_error_msg(dic):
        if "users_id" in dic.keys():
            for idx, msg in enumerate(dic["users_id"]):
                if msg.find("não é uma escolha válida para este campo.") > 0:
                    msg = msg.split("’")
                    dic["users_id"][idx] = ("Usuario Id %s’ já está associado a um contrato." % 
                                            msg[0])
        return dic

    @staticmethod
    def _populate_obj(form, entity):
        form.populate_obj(entity)
        if form.users_id.data:
            for user_id in form.users_id.data:
                if user_id not in [user.id for user in entity.users]:
                    user = UserService.read(user_id, serializer=False)
                    entity.users.append(user)
        return entity
