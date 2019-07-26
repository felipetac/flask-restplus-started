
from app.mod_common.service import BaseService
from .model import Model, Schema
from .form import Form


class Service(BaseService):
    class Meta:
        model = Model
        form = Form
        schema = Schema
