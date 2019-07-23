from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema

CONTRACT_USER = DB.Table('app_contract_user', BaseModel.metadata,
                         DB.Column('contract_id', DB.Integer,
                                   DB.ForeignKey('app_contract.id', ondelete="CASCADE"),
                                   primary_key=True),
                         DB.Column('user_id', DB.Integer,
                                   DB.ForeignKey('app_user.id', ondelete="CASCADE"),
                                   primary_key=True, unique=True))

class Model(BaseModel):

    __tablename__ = 'app_contract'

    company_name = DB.Column(DB.String(200), nullable=False)
    company_cnpj = DB.Column(DB.String(50), nullable=False, unique=True, index=True)
    active = DB.Column(DB.Boolean, nullable=False, default=True)
    base_price = DB.Column(DB.Float, nullable=True)
    users = DB.relationship(User, secondary=CONTRACT_USER,
                            backref=DB.backref('company'))

class Schema(BaseSchema):

    class Meta:
        model = Model

    users = fields.Nested(UserSchema, many=True, only=["id", "name", "email"])
