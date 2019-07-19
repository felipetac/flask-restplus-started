from marshmallow import fields
from app.mod_common.model import DB, BaseModel, BaseSchema
from app.mod_user.model import Model as User, Schema as UserSchema
from .service import Model as ServiceModel, Schema as ServiceSchema

SERVICES = DB.Table('app_bill_service', BaseModel.metadata,
                    DB.Column('id', DB.Integer, primary_key=True),
                    DB.Column(DB.DateTime, default=DB.func.current_timestamp(), index=True),
                    DB.Column('bill_id', DB.Integer,
                              DB.ForeignKey('app_bill.id'), index=True),
                    DB.Column('service_id', DB.Integer,
                              DB.ForeignKey('app_service.id'))
                   )

class Model(BaseModel):

    __tablename__ = 'app_bill'

    module_name = DB.Column(DB.String(200), nullable=False)
    class_name = DB.Column(DB.String(200), nullable=False)
    method_name = DB.Column(DB.String(200), nullable=False)
    base_url = DB.Column(DB.String(500), nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('app_user.id'),
                        nullable=True)
    user = DB.relationship(User)
    called_services = DB.relationship(ServiceModel, secondary=SERVICES,
                                      backref=DB.backref('bills'),
                                      nullable=True)
    complexity_level = DB.Column(DB.Integer, nullable=True)
    cost = DB.Column(DB.Numeric, default=0.0)

class Schema(BaseSchema):

    class Meta:
        model = Model

    user = fields.Nested(UserSchema)
    called_services = fields.Nested(ServiceSchema, many=True)
