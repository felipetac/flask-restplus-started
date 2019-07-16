
from flask_restplus import Namespace, Resource, fields
from .service import Service

API = Namespace('auth', description='Operações de Autenticação')

_USER = API.model('Login', {
    'email': fields.String(required=True, description='Email do Usuário',
                           example="carlos.silva@gmail.com"),
    'password': fields.String(required=True, description='Senha do Usuário',
                              example="minhasenha123")
})

_KEY = API.model('Key', {
    'key': fields.String(required=True, description='Chave de acesso'),
})

@API.route('/getkey')
@API.expect(_USER)
@API.response(201, 'Chave  de acesso disponibilizada', _KEY)
@API.response(400, 'Formulário inválido')
class Key(Resource):
    '''Obter a chave de acesso'''
    @API.doc('get_key')
    def post(self):
        '''Obter a chave de acesso'''
        res = Service.get_key(API.payload)
        if "form" in res.keys():
            API.abort(400, "Formulário inválido", status=res["form"], statusCode="400")
        return res["data"], 201
