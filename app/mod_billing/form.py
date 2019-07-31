from wtforms.fields import SelectField
from app.mod_common.form import RestForm
from app.mod_contract.service import Service as ContractService
from app.mod_user.service import Service as UserService
from app.mod_cost.service import Service as CostService
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model

    contract_id = SelectField('Contract Id', coerce=int,
                              choices=ContractService.get_choices("id", "name"))
    user_id = SelectField('User Id', coerce=int,
                          choices=UserService.get_choices("id", "name"))
    cost_id = SelectField('Cost Id', coerce=int,
                          choices=CostService.get_choices("id", "id"))
