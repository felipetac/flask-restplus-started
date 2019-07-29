from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema
from app.mod_contract.model import Model as Contract, Schema as ContractSchema
from app.mod_cost.model import Model as Cost, Schema as CostSchema

class Model(BaseModel):

    __tablename__ = 'app_bill'

    base_url = DB.Column(DB.String(500), nullable=False)
    contract_id = DB.Column(DB.Integer, DB.ForeignKey('app_contract.id'),
                            nullable=False, index=True)
    contract = DB.relationship(Contract, cascade="all")
    user_id = DB.Column(DB.Integer, DB.ForeignKey('app_user.id'),
                        nullable=False, index=True)
    user = DB.relationship(User, cascade="all")
    cost_id = DB.Column(DB.Integer, DB.ForeignKey('app_cost.id', ondelete="CASCADE"),
                        nullable=False, index=True)
    cost = DB.relationship(Cost, cascade="all")

class Schema(BaseSchema):

    class Meta:
        model = Model

    contract = fields.Nested(ContractSchema, only=["id", "name", "owner"])
    user = fields.Nested(UserSchema, only=["id", "name"])
    cost = fields.Nested(CostSchema, only=["id", "role", "cost"])
