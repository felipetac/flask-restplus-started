

import os
from flask import Flask, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_babel import Babel
from config import CONFIG
from flask_cors import CORS

# Define the WSGI application object
APP = Flask(__name__)

# CORS Simple Usage
CORS = CORS(APP) # TOdO: Implementar CORS Dinâmico?

# Configurations
__ENV = os.environ["FLASK_ENV"] if "FLASK_ENV" in os.environ.keys(
) else "default"
APP.config.from_object(CONFIG.get(__ENV))

with APP.app_context():
    # Chamando da configuração o esquema da senha
    PS = current_app.config['PASSWORD_SCHEMES'] or ['pbkdf2_sha512']
    # Chamando da configuração qtd. itens por pagina
    PP = current_app.config['PER_PAGE'] or 100

# Define the database object which is imported
# by modules and controllers
DB = SQLAlchemy(APP, session_options={"autoflush": False})

# Object serialization and deserialization, lightweight and fluffy
MA = Marshmallow(APP)

# Babel adds i18n and l10n support to any Flask application
BA = Babel(APP)

# Sample HTTP error handling
@APP.errorhandler(404)
def not_found(error):
    ret = error.args if error.args else "Url não encontrada..."
    return jsonify({"result": ret}), 404

def create_app(env=None):
    if not APP.blueprints.keys():

        if env and env == 'testing':
            APP.config.from_object(CONFIG.get(env))

        from app.mod_role.service import Service as RoleService

        # Register blueprint(s)
        from .api import BLUEPRINT as API
        APP.register_blueprint(API)

        # Build the database:
        # This will create the database file using SQLAlchemy
        DB.create_all()

        # Persist All roles in database
        RoleService(APP).create_all()

    return APP
