from wtforms.validators import Optional
from wtforms.fields import SelectMultipleField
from app.mod_common.form import RestForm
from app.mod_common.validator import CNPJ
from .model import Model
from .validator import UniqueRolePerCNPJ


class Form(RestForm):

    class Meta:
        model = Model
        field_args = {'company_cnpj': {'validators': [CNPJ()]}}

    users_id = SelectMultipleField('Users Ids', validators=[Optional()],
                                   coerce=int)
    roles_id = SelectMultipleField('Roles Ids',
                                   validators=[Optional(),
                                               UniqueRolePerCNPJ(Model.roles)], coerce=int)
