from flask import Blueprint
from flask_restplus import Api

BLUEPRINT = Blueprint('user_api', __name__)

API = Api(BLUEPRINT,
          version='0.1',
          title='API da Aplicação',
          description='API geral da aplicação',)

# Adicionando as rotas dos modulos

# pylint: disable=wrong-import-position
from app.mod_user.api import NS as UserNS
from app.mod_role.api import NS as RoleNS
# pylint: enable=wrong-import-position

API.add_namespace(UserNS)
API.add_namespace(RoleNS)
