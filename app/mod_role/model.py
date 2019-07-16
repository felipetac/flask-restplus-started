# Hash password Automagic
from app.mod_common.model import DB, BaseModel, BaseSchema

ROLES = DB.Table('app_user_role', BaseModel.metadata,
                 DB.Column('role_id', DB.Integer,
                           DB.ForeignKey('app_role.id'), primary_key=True),
                 DB.Column('user_id', DB.Integer,
                           DB.ForeignKey('app_user.id'), primary_key=True)
                )

class Model(BaseModel):

    __tablename__ = 'app_role'

    module_name = DB.Column(DB.String(200), nullable=False)
    class_name = DB.Column(DB.String(200), nullable=False)
    method_name = DB.Column(DB.String(200), nullable=False)
    role_name = DB.Column(DB.String(200), nullable=False, unique=True)
    role_desc = DB.Column(DB.String(200), nullable=True)

class Schema(BaseSchema):

    class Meta:
        model = Model
