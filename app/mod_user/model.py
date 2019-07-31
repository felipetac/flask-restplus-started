# Hash password Automagic
from sqlalchemy_utils import PasswordType, EmailType
from marshmallow import fields
from app import PS
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_role.model import Model as Role, Schema as RoleSchema

USER_ROLE_EXCLUDED = DB.Table('app_user_role_excluded', BaseModel.metadata,
                              DB.Column('date_created', DB.DateTime,
                                        default=DB.func.current_timestamp(), index=True),
                              DB.Column('role_id', DB.Integer,
                                        DB.ForeignKey(
                                            'app_role.id', ondelete="CASCADE"),
                                        primary_key=True),
                              DB.Column('user_id', DB.Integer,
                                        DB.ForeignKey(
                                            'app_user.id', ondelete="CASCADE"),
                                        primary_key=True, index=True)
                              )


class Model(BaseModel):

    __tablename__ = 'app_user'

    name = DB.Column(DB.String(200), nullable=False)
    email = DB.Column(EmailType, nullable=False, unique=True, index=True)
    password = DB.Column(PasswordType(onload=lambda **kwargs: dict(schemes=PS, **kwargs)),  # pylint: disable=unnecessary-lambda
                         nullable=False)
    roles_excluded = DB.relationship(Role, secondary=USER_ROLE_EXCLUDED,
                                     backref=DB.backref('users'), cascade="all")


class Schema(BaseSchema):

    class Meta:
        model = Model
        exclude = ("password", )  # Exclude password from serialization

    roles_excluded = fields.Nested(RoleSchema, many=True,
                                   only=("id", "name", ))
