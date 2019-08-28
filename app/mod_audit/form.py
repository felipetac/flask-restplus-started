from wtforms.validators import Optional
#from wtforms.fields import SelectField
from app.mod_common.form import RestForm, SelectModelField
from app.mod_user.model import Model as User
from app.mod_user.service import Service as UserService
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model

    user = SelectModelField(User, 'User Ids', validators=[Optional()],
                            coerce=int)

    def load_choices(self):
        self.user.choices = UserService.get_choices("id", "name")
