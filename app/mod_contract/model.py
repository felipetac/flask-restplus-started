from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema
from app.mod_role.model import Model as Role, Schema as RoleSchema
from app.mod_owner.model import Model as Owner, Schema as OwnerSchema

CONTRACT_USER = DB.Table('app_contract_user', BaseModel.metadata,
                         DB.Column('date_created', DB.DateTime,
                                   default=DB.func.current_timestamp(), index=True),
                         DB.Column('contract_id', DB.Integer,
                                   DB.ForeignKey(
                                       'app_contract.id', ondelete="CASCADE"),
                                   primary_key=True, index=True),
                         DB.Column('user_id', DB.Integer,
                                   DB.ForeignKey(
                                       'app_user.id', ondelete="CASCADE"),
                                   primary_key=True))

CONTRACT_ROLE = DB.Table('app_contract_role', BaseModel.metadata,
                         DB.Column('date_created', DB.DateTime,
                                   default=DB.func.current_timestamp(), index=True),
                         DB.Column('contract_id', DB.Integer,
                                   DB.ForeignKey(
                                       'app_contract.id', ondelete="CASCADE"),
                                   primary_key=True, index=True),
                         DB.Column('role_id', DB.Integer,
                                   DB.ForeignKey(
                                       'app_role.id', ondelete="CASCADE"),
                                   primary_key=True)
                         )


class Model(BaseModel):

    __tablename__ = 'app_contract'

    name = DB.Column(DB.String(200), nullable=False, unique=True)
    issuer = DB.Column(DB.String(100), nullable=False, unique=True)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey('app_contract_owner.id',
                                                   ondelete="CASCADE"),
                         nullable=False, index=True)
    owner = DB.relationship(
        Owner, backref=DB.backref('contracts'), cascade="all")
    is_active = DB.Column(DB.Boolean, nullable=False, default=True)
    is_billed = DB.Column(DB.Boolean, nullable=False, default=True)
    bill_day = DB.Column(DB.Integer, nullable=False, default=30)
    users = DB.relationship(User, secondary=CONTRACT_USER,
                            backref=DB.backref('contracts'))
    roles = DB.relationship(Role, secondary=CONTRACT_ROLE,
                            backref=DB.backref('contracts'))
    expire_at = DB.Column(DB.DateTime, nullable=True, index=True)


class Schema(BaseSchema):

    class Meta:
        model = Model

    users = fields.Nested(OwnerSchema, only=["id", "name", "cpf_cnpj"])
    users = fields.Nested(UserSchema, many=True, only=["id", "name", "email"])
    roles = fields.Nested(RoleSchema, many=True,
                          only=("id", "name", ))
