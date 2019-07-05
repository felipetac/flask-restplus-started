# Hash password Automagic
from sqlalchemy_utils import PasswordType, EmailType

from app import DB, MA, PS
from app.mod_common.model import Base

class User(Base):

    __tablename__ = 'auth_user'

    name = DB.Column(DB.String(200), nullable=False)
    email = DB.Column(EmailType, nullable=False, unique=True)
    password = DB.Column(PasswordType(
        onload=lambda **kwargs: dict(schemes=PS, **kwargs) # pylint: disable=unnecessary-lambda
    ), nullable=False)


class UserSchema(MA.ModelSchema):

    class Meta:
        model = User
        exclude = ("password", ) # Exclude password from serialization
