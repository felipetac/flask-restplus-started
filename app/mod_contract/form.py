from wtforms.validators import Optional
from wtforms.fields import SelectMultipleField
from app.mod_common.form import RestForm
from .model import Model

class Form(RestForm):

    class Meta:
        model = Model
        #field_args = {'role_name': {'filters': [to_lower]}}

    users_id = SelectMultipleField('Users Ids', validators=[Optional()], coerce=int)
