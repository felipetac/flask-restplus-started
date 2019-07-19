from app.mod_common.service import DB, BaseService
from .model import Model, Schema
from .form import Form

class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @staticmethod
    def read_by_attrs(module_name, class_name, method_name):
        res = DB.session.query(Model).filter(Model.module_name == module_name,
                                             Model.class_name == class_name,
                                             Model.method_name == method_name).first()
        return res

    @classmethod
    def get_choices(cls):
        ret = Model.query.all()
        return [(r.id, (r.class_name + "." + r.method_name)) for r in ret] if ret else None
