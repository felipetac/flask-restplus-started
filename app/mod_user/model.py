# Hash password Automagic
from sqlalchemy_utils import PasswordType, EmailType
from marshmallow import fields
from app import PS
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_role.model import ROLES, Model as Role, Schema as RoleSchema

class Model(BaseModel):

    __tablename__ = 'app_user'

    name = DB.Column(DB.String(200), nullable=False)
    email = DB.Column(EmailType, nullable=False, unique=True, index=True)
    password = DB.Column(PasswordType(
        onload=lambda **kwargs: dict(schemes=PS, **kwargs) # pylint: disable=unnecessary-lambda
    ), nullable=False)
    active = DB.Column(DB.Boolean, nullable=False, default=True)
    roles = DB.relationship(Role, secondary=ROLES,
                            backref=DB.backref('users'), cascade="all")

class Schema(BaseSchema):

    class Meta:
        model = Model
        exclude = ("password", ) # Exclude password from serialization

    roles = fields.Nested(RoleSchema, many=True,
                          only=("id", "role_name", ))
