from wtforms.validators import Optional
from wtforms.fields import SelectField
from app.mod_common.form import RestForm
from .model import Model

class Form(RestForm):

    class Meta:
        model = Model

    user_id = SelectField('Roles Ids', validators=[Optional()], coerce=int)
