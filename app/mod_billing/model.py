from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema
from app.mod_account.model import Model as Account, Schema as AccountSchema
from app.mod_role.model import Model as Role, Schema as RoleSchema


class Model(BaseModel):

    __tablename__ = 'app_bill'

    base_url = DB.Column(DB.String(500), nullable=False)
    account_id = DB.Column(DB.Integer, DB.ForeignKey('app_account.id'),
                           nullable=False, index=True)
    account = DB.relationship(Account)
    role_id = DB.Column(DB.Integer, DB.ForeignKey('app_role.id'),
                        nullable=False, index=True)
    role = DB.relationship(Role)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('app_user.id'),
                        nullable=False, index=True)
    user = DB.relationship(User)


class Schema(BaseSchema):

    class Meta:
        model = Model

    account = fields.Nested(AccountSchema, only=["id", "name", "code_name"])
    role = fields.Nested(RoleSchema, only=["id", "name"])
    user = fields.Nested(UserSchema, only=["id", "name"])
