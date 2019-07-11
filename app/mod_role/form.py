from app.mod_common.sanitizer import to_lower
from app.mod_common.form import RestForm
from .model import Role as RoleModel

class Role(RestForm):

    class Meta:
        model = RoleModel
        field_args = {'name': {'filters': [to_lower]}}
