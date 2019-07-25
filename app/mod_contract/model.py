from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema
from app.mod_role.model import Model as Role, Schema as RoleSchema

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

    company_name = DB.Column(DB.String(200), nullable=False)
    company_cnpj = DB.Column(
        DB.String(50), nullable=False, index=True)
    active = DB.Column(DB.Boolean, nullable=False, default=True)
    base_price = DB.Column(DB.Float, nullable=True)
    users = DB.relationship(User, secondary=CONTRACT_USER,
                            backref=DB.backref('companies'))
    roles = DB.relationship(Role, secondary=CONTRACT_ROLE,
                            backref=DB.backref('companies'))


class Schema(BaseSchema):

    class Meta:
        model = Model

    users = fields.Nested(UserSchema, many=True, only=["id", "name", "email"])
    roles = fields.Nested(RoleSchema, many=True,
                          only=("id", "role_name", ))
