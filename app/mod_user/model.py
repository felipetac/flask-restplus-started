# Hash password Automagic
from sqlalchemy_utils import PasswordType, EmailType
from marshmallow import fields
from app import PS
from app.mod_common.model import DB, Base, Schema
from app.mod_role.model import ROLES, RoleSchema

class User(Base):

    __tablename__ = 'app_user'

    name = DB.Column(DB.String(200), nullable=False)
    email = DB.Column(EmailType, nullable=False, unique=True)
    password = DB.Column(PasswordType(
        onload=lambda **kwargs: dict(schemes=PS, **kwargs) # pylint: disable=unnecessary-lambda
    ), nullable=False)
    roles = DB.relationship('Role', secondary=ROLES,
                            backref=DB.backref('users'))

class UserSchema(Schema):

    class Meta:
        model = User
        exclude = ("password", ) # Exclude password from serialization

    roles = fields.Nested(RoleSchema, many=True,
                          only=("id", "role_name", ))
