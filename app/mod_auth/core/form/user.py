from wtforms.validators import Optional
from wtforms.fields import SelectField
from app.mod_auth.core.model.user import User
from app.mod_auth.core.sanitizer import to_lower
from . import RestForm


class UserForm(RestForm):

    class Meta:
        model = User
        field_args = {'email': {'filters': [lambda x: x, to_lower]}}

    group_id = SelectField('Group Id', validators=[Optional()], coerce=int)
