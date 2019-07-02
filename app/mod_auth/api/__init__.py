from flask import Blueprint
from flask_restplus import Api

BLUEPRINT = Blueprint('api', __name__)
API = Api(BLUEPRINT,
          version='1.0',
          title='TodoMVC API',
          description='A simple TodoMVC API',)

from app.mod_auth.api.user import NS # pylint: disable=wrong-import-position
API.add_namespace(NS)
