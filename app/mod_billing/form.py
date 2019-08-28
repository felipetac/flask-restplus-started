#from wtforms.fields import SelectField
from app.mod_common.form import RestForm, SelectModelField
from app.mod_account.model import Model as Account
from app.mod_user.model import Model as User
from app.mod_role.model import Model as Role
from app.mod_account.service import Service as AccountService
from app.mod_user.service import Service as UserService
from app.mod_role.service import Service as RoleService
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model

    account = SelectModelField(Account, 'account Role Id', coerce=int,
                               choices=AccountService.get_choices("id", "code_name"))
    role = SelectModelField(Role, 'Role Id', coerce=int,
                            choices=RoleService.get_choices("id", "name"))
    user = SelectModelField(User, 'User Id', coerce=int,
                            choices=UserService.get_choices("id", "name"))

#ToDo: Repensar implementação utilizando a tabela app_account_role ??
