from app.mod_auth.core.model.user import User
from app.mod_auth.core.sanitizer import to_lower
from . import RestForm


class UserForm(RestForm):

    class Meta:
        model = User
        field_args = {'email': {'filters': [lambda x: x, to_lower]}}
