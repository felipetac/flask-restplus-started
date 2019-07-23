# Hash password Automagic
from app.mod_common.model import DB, BaseModel, BaseSchema

USER_ROLE = DB.Table('app_user_role', BaseModel.metadata,
                 DB.Column('role_id', DB.Integer,
                           DB.ForeignKey('app_role.id', ondelete="CASCADE"),
                                         primary_key=True),
                 DB.Column('user_id', DB.Integer,
                           DB.ForeignKey('app_user.id', ondelete="CASCADE"),
                                         primary_key=True, index=True)
                )

class Model(BaseModel):

    __tablename__ = 'app_role'

    module_name = DB.Column(DB.String(200), nullable=False)
    class_name = DB.Column(DB.String(200), nullable=False)
    method_name = DB.Column(DB.String(200), nullable=False)
    role_name = DB.Column(DB.String(200), nullable=False, unique=True)
    role_desc = DB.Column(DB.String(200), nullable=True)

    __table_args__ = (DB.Index("ix_app_role", "module_name", "class_name",
                               "method_name", unique=True),)

class Schema(BaseSchema):

    class Meta:
        model = Model
