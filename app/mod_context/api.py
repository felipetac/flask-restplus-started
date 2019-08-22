from flask_restplus import Namespace, Resource, fields
from app.mod_role.service import Service as ROLE
from .service import Service

AUTHORIZATIONS = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

API = Namespace('context', description='Operações de Contexto para Aplicação')

_CONTEXT = API.model('Context', {
    'nome': fields.String(required=True, description='Nome do Contexto da Aplicação',
                          example="app-xpto"),
    'description': fields.String(required=True, description='Descrição do Contexto da Aplicação',
                                 example="Aplicação XPTO para gerenciamento XPTO"),
    'key_exp': fields.Integer(required=True,
                                  description='Tempo de expiração da Chave de Acesso (em segundos)',
                                  example="1800"),
    'contexts_id': fields.List(fields.Integer(required=False,
                                              description='Lista de ids das Regras de Contrato')),
})


@ROLE.register
@API.route('/')
@API.expect(_CONTEXT)
@API.response(201, 'Chave  de acesso disponibilizada', _CONTEXT)
@API.response(400, 'Formulário inválido')
class Context(Resource):
    '''Criar Contexto de Aplicação'''
    @API.doc('create_context')
    def post(self):
        '''Criar Contexto de Aplicação'''
        res = Service.get_key(API.payload)
        if "form" in res.keys():
            API.abort(400, "Formulário inválido",
                      status=res["form"], statusCode="400")
        return res["data"], 201
