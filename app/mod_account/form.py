import random
from wtforms.validators import Optional, NumberRange
from wtforms.fields import SelectField, SelectMultipleField
from app.mod_common.form import RestForm
from app.mod_user.service import Service as UserService
from app.mod_role.service import Service as RoleService
from .model import Model
from .validator import UniqueRolePerCNPJ


class Form(RestForm):

    class Meta:
        model = Model
        field_args = {'bill_day': {'validators': [NumberRange(min=1, max=30)]},
                      'expire_at': {'format': '%d/%m/%Y %H:%M:%S'}}

    owner_id = SelectField('Owner Id', coerce=int,
                           choices=UserService.get_choices("id", "name"))
    users_id = SelectMultipleField('Users Ids',
                                   validators=[Optional()], coerce=int,
                                   choices=UserService.get_choices("id", "name"))
    roles_id = SelectMultipleField('Roles Ids', validators=[Optional(),
                                                            UniqueRolePerCNPJ(
                                                                Model.roles)], coerce=int,
                                   choices=RoleService.get_choices("id", "name"))

    def populate_obj(self, entity):
        if self.name.data:
            entity.name = self.name.data
        if self.expire_at.data:
            entity.expire_at = self.expire_at.data
        if not entity.code_name:
            entity.code_name = self._create_code_name()
        if self.key_exp.data:
            entity.key_exp = self.key_exp.data
        if self.owner_id.data:
            owner = UserService.read(self.owner_id.data, serialize=False)
            if owner:
                entity.owner = owner
        if self.users_id.data:
            for user_id in self.users_id.data:
                if user_id not in [user.id for user in entity.users]:
                    user = UserService.read(user_id, serialize=False)
                    entity.users.append(user)
        if self.roles_id.data:
            for role_id in self.roles_id.data:
                if role_id not in [role.id for role in entity.roles]:
                    role = RoleService.read(role_id, serialize=False)
                    entity.roles.append(role)

    @classmethod
    def _create_code_name(cls):
        from .service import Service  # Inner Import para evitar import cíclico
        _hash = random.getrandbits(16)
        code_name = "conta-%s" % _hash
        if not Service.read_by_code(code_name):
            return code_name
        return cls._create_code_name()
