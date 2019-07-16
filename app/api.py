from flask import Blueprint
from flask_restplus import Api

# pylint: disable=wrong-import-position
from app.mod_user.api import API as UserNS
from app.mod_role.api import API as RoleNS
from app.mod_auth.api import API as AuthNS
from app.mod_audit.api import API as AuditNS
# pylint: enable=wrong-import-position

BLUEPRINT = Blueprint('user_api', __name__, url_prefix='/api/1')

API = Api(BLUEPRINT,
          version='0.1',
          title='API da Aplicação',
          description='API geral da aplicação',)

# Adicionando as rotas dos modulos
API.add_namespace(UserNS)
API.add_namespace(RoleNS)
API.add_namespace(AuthNS)
API.add_namespace(AuditNS)
