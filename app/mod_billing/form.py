#from wtforms.fields import SelectField
from app.mod_common.form import RestForm, SelectModelField
from app.mod_account.model import AccountRole
from app.mod_user.model import Model as User
from app.mod_account.service import Service as AccountService
from app.mod_user.service import Service as UserService
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model

    account_role = SelectModelField(AccountRole, 'Account Role Id', coerce=int)
    user = SelectModelField(User, 'User Id', coerce=int)

    def load_choices(self):
        self.account_role.choices = AccountService.get_account_role_choices()
        self.user.choices = UserService.get_choices("id", "name")
