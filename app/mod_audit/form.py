from wtforms.validators import Optional
from wtforms.fields import SelectField
from app.mod_common.form import RestForm
from app.mod_user.service import Service as UserService
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model

    user_id = SelectField('Roles Ids', validators=[Optional()],
                          coerce=int, choices=UserService.get_choices("id", "name"))

    def populate_obj(self, entity):
        if self.user_id.data:
            user = UserService.read(self.user_id.data, serialize=False)
            entity.user = user
        super().populate_obj(entity)
