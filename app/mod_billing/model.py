from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema
from app.mod_account.model import AccountRole, AccountRoleSchema


class Model(BaseModel):

    __tablename__ = 'app_bill'

    base_url = DB.Column(DB.String(500), nullable=False)
    account_role_id = DB.Column(DB.Integer, DB.ForeignKey('app_account_role.id'),
                                nullable=False, index=True)
    account_role = DB.relationship(AccountRole)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('app_user.id'),
                        nullable=False, index=True)
    user = DB.relationship(User)
    cost = DB.Column(DB.Float, nullable=True)


class Schema(BaseSchema):

    class Meta:
        model = Model

    account_role = fields.Nested(AccountRoleSchema, only=["account", "role"])
    user = fields.Nested(UserSchema, only=["id", "name", "cpf_cnpj"])
