from urllib import parse
from functools import wraps
from flask import Blueprint, request
from flask_restplus import Api

def marshal_paginate(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = function(*args, **kwargs)
        print(data)
        if "page" in data.keys():
            for k in ["curr", "prev", "next", "last"]:
                if k in data["page"].keys() and data["page"][k]:
                    print("RESULTTTTT", data["page"][k])
                    data["page"][k] = parse.urljoin(request.base_url, str(data["page"][k]))
        return data
    return wrapper

BLUEPRINT = Blueprint('api', __name__)
API = Api(BLUEPRINT,
          version='0.1',
          title='Mod. Auth API',
          description='API do módulo de autenticação do usuário',)

from app.mod_auth.api.user import NS # pylint: disable=wrong-import-position
API.add_namespace(NS)
