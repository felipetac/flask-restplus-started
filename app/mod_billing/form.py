from wtforms.fields import SelectField
from app.mod_common.form import RestForm
from app.mod_account.service import Service as AccountService
from app.mod_user.service import Service as UserService
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model

    account_id = SelectField('account Role Id', coerce=int,
                             choices=AccountService.get_choices("id", "name"))
    user_id = SelectField('User Id', coerce=int,
                          choices=UserService.get_choices("id", "name"))
