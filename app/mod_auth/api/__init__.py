from flask import Blueprint
from flask_restplus import Api

BLUEPRINT = Blueprint('api', __name__)
API = Api(BLUEPRINT,
          version='0.1',
          title='Mod. Auth API',
          description='API do módulo de autenticação do usuário',)

from app.mod_auth.api.user import NS # pylint: disable=wrong-import-position
API.add_namespace(NS)
