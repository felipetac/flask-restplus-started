from app.mod_common.service import DB, BaseService
from .model import Model, Schema
from .form import Form

ROLES_REGISTRY = []


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema
        # order_by = "id" #caso queira mudar
        # sort = "desc" #caso queira mudar

    def __init__(self, app):
        self.app = app

    @classmethod
    def read_by_attrs(cls, module_name, class_name, method_name):
        model = cls.Meta.model
        res = DB.session.query(model).filter(model.module_name == module_name,
                                             model.class_name == class_name,
                                             model.method_name == method_name).first()
        return res

    def create_all(self):
        roles = []
        with self.app.app_context():
            for obj in ROLES_REGISTRY:
                if not self.read_by_attrs(obj["module_name"], obj["class_name"],
                                          obj["method_name"]):
                    roles.append(self.create(obj))
        return roles
