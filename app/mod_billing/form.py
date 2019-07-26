from wtforms.fields import SelectField
from app.mod_common.form import RestForm
from .model import Bill, Cost


class CostForm(RestForm):

    class Meta:
        model = Cost

    role_id = SelectField('Role Id', coerce=int)


class BillForm(RestForm):

    class Meta:
        model = Bill

    contract_id = SelectField('Contracts Id', coerce=int)
    user_id = SelectField('User Id', coerce=int)
    cost_id = SelectField('Cost Id', coerce=int)
