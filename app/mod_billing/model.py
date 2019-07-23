from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema
from app.mod_contract.model import Model as Contract, Schema as ContractSchema
from app.mod_service.model import Model as ServiceModel, Schema as ServiceSchema

BILL_SERVICE = DB.Table('app_bill_service', BaseModel.metadata,
                    DB.Column('id', DB.Integer, primary_key=True),
                    DB.Column('date_created', DB.DateTime,
                              default=DB.func.current_timestamp(), index=True),
                    DB.Column('bill_id', DB.Integer,
                              DB.ForeignKey('app_bill.id', ondelete="CASCADE"), index=True),
                    DB.Column('service_id', DB.Integer,
                              DB.ForeignKey('app_service.id', ondelete="CASCADE"))
                   )

class Model(BaseModel):

    __tablename__ = 'app_bill'

    module_name = DB.Column(DB.String(200), nullable=False)
    class_name = DB.Column(DB.String(200), nullable=False)
    method_name = DB.Column(DB.String(200), nullable=False)
    base_url = DB.Column(DB.String(500), nullable=False)
    contract_id = DB.Column(DB.Integer, DB.ForeignKey('app_contract.id'),
                            nullable=True, index=True)
    contract = DB.relationship(Contract, cascade="all")
    user_id = DB.Column(DB.Integer, DB.ForeignKey('app_user.id'),
                        nullable=True, index=True)
    user = DB.relationship(User, cascade="all")
    called_services = DB.relationship(ServiceModel, secondary=BILL_SERVICE,
                                      backref=DB.backref('bills'), cascade="all")
    complexity_level = DB.Column(DB.Integer, nullable=True)
    cost = DB.Column(DB.Numeric, default=0.0)

    __table_args__ = (DB.Index("ix_app_bill_service", "module_name", "class_name", "method_name"),)

class Schema(BaseSchema):

    class Meta:
        model = Model

    contract = fields.Nested(ContractSchema, only=["id", "company_name", "company_cnpj"])
    user = fields.Nested(UserSchema, only=["id", "name"])
    called_services = fields.Nested(ServiceSchema, many=True,
                                    only=["module_name", "class_name", "method_name"])
