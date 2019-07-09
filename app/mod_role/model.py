# Hash password Automagic
from app import DB, MA
from app.mod_common.model import Base

ROLES = DB.Table('app_user_role', Base.metadata,
                 DB.Column('role_id', DB.Integer,
                           DB.ForeignKey('app_role.id'), primary_key=True),
                 DB.Column('user_id', DB.Integer,
                           DB.ForeignKey('app_user.id'), primary_key=True)
                )

class Role(Base):

    __tablename__ = 'app_role'

    module_name = DB.Column(DB.String(200), nullable=False)
    class_name = DB.Column(DB.String(200), nullable=False)
    method_name = DB.Column(DB.String(200), nullable=False)
    role_name = DB.Column(DB.String(200), nullable=False, unique=True)
    role_desc = DB.Column(DB.String(200), nullable=True)

class RoleSchema(MA.ModelSchema):

    class Meta:
        model = Role
