from app.mod_common.service import DB, BaseService
from .model import Model, Schema
from .form import Form

class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema
        #order_by = "id" #caso queira mudar
        #sort = "desc" #caso queira mudar

    @staticmethod
    def read_by_attrs(module_name, class_name, method_name):
        res = DB.session.query(Model).filter(Model.module_name == module_name,
                                             Model.class_name == class_name,
                                             Model.method_name == method_name).first()
        return res

    @classmethod
    def get_choices(cls):
        roles = Model.query.all()
        return [(r.id, r.role_name) for r in roles]
