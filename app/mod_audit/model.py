from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema

class Model(BaseModel):

    __tablename__ = 'app_audit'

    module_name = DB.Column(DB.String(200), nullable=False)
    class_name = DB.Column(DB.String(200), nullable=False)
    method_name = DB.Column(DB.String(200), nullable=False)
    base_url = DB.Column(DB.String(200), nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('app_user.id'),
                        nullable=True)
    user = DB.relationship(User)

class Schema(BaseSchema):

    class Meta:
        model = Model

    user = fields.Nested(UserSchema)
