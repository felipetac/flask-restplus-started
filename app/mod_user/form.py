from app.mod_user.model import User as UserModel
from app.mod_common.sanitizer import to_lower
from app.mod_common.form import RestForm


class User(RestForm):

    class Meta:
        model = UserModel
        field_args = {'email': {'filters': [to_lower]}}
