from app.mod_common.service import DB, BaseService
from app.mod_service.util import Util as SERVICE
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
    @SERVICE.compose
    def list(cls, page=None, per_page=None, order_by=None, sort=None):
        return super().list(page, per_page, order_by, sort)

    @classmethod
    @SERVICE.compose
    def read(cls, entity_id, serializer=True):
        return super().read(entity_id, serializer)

    @classmethod
    @SERVICE.compose
    def delete(cls, entity_id):
        return super().delete(entity_id)

    @classmethod
    @SERVICE.compose
    def create(cls, json_obj, serializer=True):
        return super().create(json_obj, serializer)

    @classmethod
    @SERVICE.compose
    def update(cls, entity_id, json_obj, serializer=True):
        return super().update(entity_id, json_obj, serializer)

    @classmethod
    @SERVICE.compose
    def get_choices(cls):
        return Model.query.with_entities(Model.id, Model.role_name).all()

    @staticmethod
    def read_by_attrs(module_name, class_name, method_name):
        res = DB.session.query(Model).filter(Model.module_name == module_name,
                                             Model.class_name == class_name,
                                             Model.method_name == method_name).first()
        return res

    @staticmethod
    def truncate():
        Model.query.delete()
