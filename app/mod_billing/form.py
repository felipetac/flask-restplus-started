from wtforms.fields import SelectField
from app.mod_common.form import RestForm
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model

    contract_id = SelectField('Contracts Id', coerce=int)
    user_id = SelectField('User Id', coerce=int)
    cost_id = SelectField('Cost Id', coerce=int)
