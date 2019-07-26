from wtforms.validators import Optional
from wtforms.fields import SelectMultipleField
from app.mod_common.sanitizer import to_lower
from app.mod_common.form import RestForm
from app.mod_role.service import Service as RoleService
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model
        field_args = {'email': {'filters': [to_lower]}}

    roles_excluded_id = SelectMultipleField(
        'Roles Excluded Ids',
        validators=[Optional()], choices=RoleService.get_choices("id", "name"), coerce=int)

    def populate_obj(self, entity):
        if self.roles_excluded_id.data:
            for role_id in self.roles_excluded_id.data:
                if role_id not in [role.id for role in entity.roles]:
                    role = RoleService.read(role_id, serializer=False)
                    entity.roles.append(role)
        super().populate_obj(entity)
