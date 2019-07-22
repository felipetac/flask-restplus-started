from wtforms.validators import Optional
from wtforms.fields import SelectMultipleField
from app.mod_common.form import RestForm
from .model import Model

class Form(RestForm):

    class Meta:
        model = Model

    users_id = SelectMultipleField('Users Ids', validators=[Optional()],
                                   coerce=int)
