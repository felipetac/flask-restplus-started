from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema
from app.mod_role.model import Model as Role, Schema as RoleSchema

ACCOUNT_USER = DB.Table(
    'app_account_user', BaseModel.metadata,
    DB.Column('date_created', DB.DateTime,
              default=DB.func.current_timestamp(), index=True),
    DB.Column('account_id', DB.Integer,
              DB.ForeignKey(
                  'app_account.id', ondelete="CASCADE"),
              primary_key=True, index=True),
    DB.Column('user_id', DB.Integer,
              DB.ForeignKey(
                  'app_user.id', ondelete="CASCADE"),
              primary_key=True))

'''ACCOUNT_ROLE = DB.Table(
    'app_account_role', BaseModel.metadata,
    DB.Column('date_created', DB.DateTime,
              default=DB.func.current_timestamp(), index=True),
    DB.Column('account_id', DB.Integer,
              DB.ForeignKey(
                  'app_account.id', ondelete="CASCADE"),
              primary_key=True, index=True),
    DB.Column('role_id', DB.Integer,
              DB.ForeignKey(
                  'app_role.id', ondelete="CASCADE"),
              primary_key=True))'''


class AccountRole(BaseModel):

    __tablename__ = 'app_account_role'

    account_id = DB.Column(DB.Integer, DB.ForeignKey('app_account.id'))
    account = DB.relationship("app.mod_account.model.Model")
    role_id = DB.Column(DB.Integer, DB.ForeignKey('app_role.id'))
    role = DB.relationship(Role, backref=DB.backref('accounts'))
    cost = DB.Column(DB.Float, nullable=True, default=0.0)

    __table_args__ = (DB.UniqueConstraint(
        'account_id', 'role_id', name='uix_app_account_role'),)


class Model(BaseModel):

    __tablename__ = 'app_account'

    name = DB.Column(DB.String(200), nullable=False, unique=True)
    code_name = DB.Column(DB.String(50), nullable=True, unique=True)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey('app_user.id'),
                         nullable=False, index=True)
    owner = DB.relationship(User, backref=DB.backref('accounts_owner'))
    is_active = DB.Column(DB.Boolean, nullable=False, default=True)
    is_billed = DB.Column(DB.Boolean, nullable=False, default=True)
    bill_day = DB.Column(DB.Integer, nullable=False, default=30)
    users = DB.relationship(User, secondary=ACCOUNT_USER,
                            backref=DB.backref('accounts'))
    roles = DB.relationship("AccountRole")
    expire_at = DB.Column(DB.DateTime, nullable=True, index=True)
    key_exp = DB.Column(DB.Integer, nullable=False)


class AccountRoleSchema(BaseSchema):

    class Meta:
        model = AccountRole

    account = fields.Nested("app.mod_account.model.Schema", only=["id", "code_name"])
    role = fields.Nested(RoleSchema, only=["id", "name"])


class Schema(BaseSchema):

    class Meta:
        model = Model

    owner = fields.Nested(UserSchema,
                          only=["id", "name", "email", "cpf_cnpj"])
    users = fields.Nested(UserSchema, many=True,
                          only=["id", "name", "email", "cpf_cnpj"])
    roles = fields.Nested(AccountRoleSchema, many=True, only=["role", "cost"])
