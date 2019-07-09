from wtforms.validators import Optional
from wtforms.fields import SelectMultipleField
from app.mod_common.sanitizer import to_lower
from app.mod_common.form import RestForm
from .model import User as UserModel

class User(RestForm):

    class Meta:
        model = UserModel
        field_args = {'email': {'filters': [to_lower]}}

    roles_id = SelectMultipleField('Roles Ids', validators=[Optional()], coerce=int)
