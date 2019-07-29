from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_role.model import Model as Role, Schema as RoleSchema


class Model(BaseModel):

    __tablename__ = 'app_cost'

    role_id = DB.Column(DB.Integer, DB.ForeignKey('app_role.id', ondelete="CASCADE"),
                        nullable=False, index=True, unique=True)
    role = DB.relationship(Role, cascade="all")
    cost = DB.Column(DB.Float, nullable=False, default=0.0)

class Schema(BaseSchema):

    class Meta:
        model = Model

    role = fields.Nested(RoleSchema, only=["id", "name"])
