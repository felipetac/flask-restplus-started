from app.mod_common.service import BaseService
from app.mod_user.service import Service as UserService
from .model import DB, Model, Schema
from .form import Form

class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema
