import random
from wtforms.validators import Optional, NumberRange
from wtforms.fields import SelectMultipleField
from app.mod_common.form import RestForm, SelectModelField, SelectMultipleModelField
from app.mod_user.model import Model as User
from app.mod_user.service import Service as UserService
from app.mod_role.service import Service as RoleService
from .model import Model, AccountRole


class Form(RestForm):

    class Meta:
        model = Model
        field_args = {'bill_day': {'validators': [NumberRange(min=1, max=30)]},
                      'expire_at': {'format': '%d/%m/%Y %H:%M:%S'}}

    owner = SelectModelField(User, 'Owner Id', coerce=int)
    users = SelectMultipleModelField(User, 'Users Ids',
                                     validators=[Optional()], coerce=int)
    roles = SelectMultipleField('Roles Ids',
                                validators=[Optional()],
                                coerce=int)

    def load_choices(self):
        u_choices = UserService.get_choices("id", "name")
        self.owner.choices = u_choices
        self.users.choices = u_choices
        self.roles.choices = RoleService.get_choices("id", "name")

    #pylint: disable=no-member
    def populate_obj(self, entity):
        if not self.code_name.data:
            self.code_name.data = self._create_code_name()
        if self.roles.data:
            arr = []
            for role_id in self.roles.data:
                assoc = AccountRole()
                role = RoleService.read(role_id, serialize=False)
                if role:
                    assoc.role = role
                    arr.append(assoc)
            self.roles.data = arr
        RestForm.populate_obj(self, entity)
    #pylint: enable=no-member

    @classmethod
    def _create_code_name(cls):
        _hash = random.getrandbits(16)
        code_name = "conta-%s" % _hash
        model = cls.Meta.model()
        entity = model.query.filter_by(code_name=code_name).first()
        if not entity:
            return code_name
        return cls.create_code_name()
