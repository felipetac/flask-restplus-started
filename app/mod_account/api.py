from flask_restplus import Namespace, Resource, fields
from app.mod_role.service import Service as ROLE
from app.mod_audit.service import Service as AUDIT
from app.mod_auth.service import Service as AUTH
from app.mod_auth.api import AUTHORIZATIONS
from app.mod_common.util import Util
from .service import Service as ACCOUNT

API = Namespace('account', description='Operações da Conta',
                authorizations=AUTHORIZATIONS)

_ACCOUNT = API.model('Account', {
    'name': fields.String(required=True, description='Nome da conta',
                          example="Conta XPTO"),
    'owner_id': fields.Integer(required=True, description='Id do Responsável da conta'),
    'is_active': fields.Boolean(required=True, description='Conta ativa?', example=True),
    'is_billed': fields.Boolean(required=True, description='Conta bilhetável?', example=True),
    'bill_day': fields.Integer(required=True, description='Dia de fechamento da fatura',
                               example=10),
    'users_id': fields.List(fields.Integer(required=False,
                                           description='Lista de ids dos usuários')),
    'roles_id': fields.List(fields.Integer(required=False,
                                           description='Lista de ids das regras')),
    'expire_at': fields.DateTime(required=False, description="Data expiração da conta",
                                 example=Util.datetime_delta(864000)),
    'key_exp': fields.Integer(required=True,
                              description='Tempo de expiração do token (em segundos)', example=420)
})


@ROLE.register
@API.route('/')
class Account(Resource):
    '''Cria um novo usuario'''
    @API.doc('create_account')
    @API.doc(security='jwt')
    @API.expect(_ACCOUNT)
    @API.response(201, 'Conta criada', _ACCOUNT)
    @API.response(400, 'Formulário inválido')
    # @API.marshal_with(_ACCOUNT, code=201)
    # @AUTH.required
    @AUDIT.register
    def post(self):
        '''Cria um nova conta'''
        res = ACCOUNT.create(API.payload)
        if "form" in res.keys():
            API.abort(400, "Formulário inválido",
                      status=res["form"], statusCode="400")
        return res, 201


@ROLE.register
@API.route('/<int:_id>')
@API.response(404, 'Conta não encontrada')
@API.param('_id', 'Identificador do conta')
class AccountItem(Resource):
    '''Exibe um conta e permite a manipulação do mesmo'''
    @API.doc('get_account')
    @API.doc(security='jwt')
    # @API.marshal_with(_ACCOUNT)
    @API.response(200, 'Conta apresentada', _ACCOUNT)
    @AUTH.required
    @AUDIT.register
    def get(self, _id):
        '''Exibe um conta dado seu identificador'''
        res = ACCOUNT.read(_id)
        if not res:
            API.abort(400, "Conta não encontrada",
                      status={"id": _id}, statusCode="404")
        return res

    @API.doc('delete_account')
    @API.doc(security='jwt')
    @API.response(204, 'Conta apagada')
    @AUTH.required
    @AUDIT.register
    def delete(self, _id):
        '''Apaga um conta dado seu identificador'''
        res = ACCOUNT.delete(_id)
        if not res:
            API.abort(400, "Conta não encontrado",
                      status={"id": _id}, statusCode="404")
        return "Conta apagada com sucesso!", 204

    @API.doc('update_account')
    @API.doc(security='jwt')
    @API.expect(_ACCOUNT)
    @API.response(200, 'Conta atualizada', _ACCOUNT)
    # @API.marshal_with(_ACCOUNT, code=200)
    # @AUTH.required
    @AUDIT.register
    def put(self, _id):
        '''Atualiza um conta dado seu identificador'''
        res = ACCOUNT.update(_id, API.payload)
        if not res:
            API.abort(400, "Conta não encontrada",
                      status={"id": _id}, statusCode="404")
        return res


@ROLE.register
@API.route('/page/<int:page>',
           '/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/<string:sort>/limit/<int:per_page>/page/<int:page>')
@API.response(200, 'Conta listado')
@API.response(404, 'URL inválida')
@API.param('page', 'Numero da página')
@API.param('per_page', 'Quantidade de contas por página')
@API.param('order_by', 'Atributo de ordenação')
@API.param('sort', 'Tipo da ordenação')
class AccountPaginate(Resource):
    '''Lista as contas com paginação'''
    @API.doc('list_accounts')
    @API.doc(security='jwt')
    # @API.marshal_list_with(_ACCOUNT)
    #@AUTH.required
    @AUDIT.register
    @ACCOUNT.marshal_paginate
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista as contas com paginação'''
        res = ACCOUNT.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            API.abort(404, "URL inválida",
                      status=res["form"], statusCode="400")
        return res
