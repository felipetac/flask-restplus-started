from app.mod_common.service import BaseService
from .model import Model, Schema
from .form import Form


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def read_by_code(cls, code_name, serialize=True):
        if code_name and isinstance(code_name, str):
            entity = cls.Meta.model.query.filter_by(
                code_name=code_name).first()
            if entity:
                if serialize:
                    entity_schema = cls.Meta.schema()
                    return entity_schema.dump(entity)
                return entity
        return None
