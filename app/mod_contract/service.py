from app.mod_common.service import BaseService
from .model import DB, Model, Schema
from .form import Form


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def read_by_issuer(cls, issuer):
        model = cls.Meta.model
        res = DB.session.query(model).filter(
            model.issuer == issuer).first()
        return res
