from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_contract.model import ContractRole, ContractRoleSchema

CONTEXT = DB.Table('app_context_join', BaseModel.metadata,
                   DB.Column('date_created', DB.DateTime,
                             default=DB.func.current_timestamp(), index=True),
                   DB.Column('context_id', DB.Integer,
                             DB.ForeignKey(
                                 'app_context.id', ondelete="CASCADE"),
                             primary_key=True),
                   DB.Column('contract_role_id', DB.Integer,
                             DB.ForeignKey(
                                 'app_contract_role.id', ondelete="CASCADE"),
                             primary_key=True)
                   )


class Model(BaseModel):

    __tablename__ = 'app_context'

    name = DB.Column(DB.String(200), nullable=False, unique=True)
    description = DB.Column(DB.String(200), nullable=True)
    issuer = DB.Column(DB.String(100), nullable=True, unique=True)
    key_exp = DB.Column(DB.Integer, nullable=True)
    contexts = DB.relationship(ContractRole, secondary=CONTEXT, cascade="all")

class Schema(BaseSchema):

    class Meta:
        model = Model

    contexts = fields.Nested(ContractRoleSchema, many=True)
