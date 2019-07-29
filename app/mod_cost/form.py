from wtforms.fields import SelectField
from app.mod_common.form import RestForm
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model

    role_id = SelectField('Role Id', coerce=int)
