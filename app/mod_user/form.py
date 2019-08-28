from wtforms.validators import Optional
#from wtforms.fields import SelectMultipleField
from app.mod_common.sanitizer import to_lower
from app.mod_common.form import RestForm, SelectMultipleModelField
from app.mod_common.validator import Unique, CPFCNPJ
from app.mod_role.model import Model as Role
from app.mod_role.service import Service as RoleService
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model
        field_args = {'email': {'filters': [to_lower]},
                      'cpf_cnpj': {'validators': [CPFCNPJ(), Unique(model.cpf_cnpj)]}}

    roles_excluded = SelectMultipleModelField(
        Role, 'Roles Excluded Ids', validators=[Optional()], coerce=int)

    def load_choices(self):
        self.roles_excluded.choices = RoleService.get_choices("id", "name")
