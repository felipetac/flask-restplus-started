from app.mod_common.service import BaseService
from .model import Model, Schema
from .form import Form


class Service(BaseService):

    class Meta:
        model = Model
        form = Form
        schema = Schema

    @classmethod
    def get_by_email(cls, email, serializer=True):
        if email and isinstance(email, str):
            user = Model.query.filter_by(email=email).first()
            if user:
                if serializer:
                    user_schema = Schema()
                    return {"data": user_schema.dump(user)}
                return user
        return None
