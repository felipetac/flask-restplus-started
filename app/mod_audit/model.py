from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema

class Model(BaseModel):

    __tablename__ = 'app_audit'

    module_name = DB.Column(DB.String(200), nullable=False)
    class_name = DB.Column(DB.String(200), nullable=False)
    method_name = DB.Column(DB.String(200), nullable=False)
    base_url = DB.Column(DB.String(200), nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('app_user.id', ondelete="CASCADE"),
                        nullable=True, index=True)
    user = DB.relationship(User, cascade="all")

    __table_args__ = (DB.Index("ix_app_audit_service", module_name, class_name, method_name),)

class Schema(BaseSchema):

    class Meta:
        model = Model

    user = fields.Nested(UserSchema)
