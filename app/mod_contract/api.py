from flask_restplus import Namespace, Resource, fields
from app.mod_common.util import Util as UTIL
from app.mod_role.util import Util as ROLE
from app.mod_audit.util import Util as AUDIT
from app.mod_auth.util import Util as AUTH
from app.mod_auth.api import AUTHORIZATIONS
from .service import Service

API = Namespace('contract', description='Operações do Contrato',
                authorizations=AUTHORIZATIONS)

_CONTRACT = API.model('Contract', {
    'company_name': fields.String(required=True, description='Nome do contrato',
                                  example="Empresa XPTO"),
    'company_cnpj': fields.String(required=True, description='CNPJ do contrato',
                                  example="97.953.939/0001-02"),
    'active': fields.Boolean(required=True, description='Contrato ativo', example=True),
    'base_price': fields.Float(description='Valor base da requisição', example=0.02345),
    'users_id': fields.List(fields.Integer(required=False,
                                           description='Lista de ids dos usuários')),
    'roles_id': fields.List(fields.Integer(required=False,
                                           description='Lista de ids das regras'))
})


@ROLE.register
@API.route('/')
class Contract(Resource):
    '''Cria um novo usuario'''
    @API.doc('create_contract')
    @API.doc(security='jwt')
    @API.expect(_CONTRACT)
    @API.response(201, 'Contrato criado', _CONTRACT)
    @API.response(400, 'Formulário inválido')
    # @API.marshal_with(_CONTRACT, code=201)
    # @AUTH.role_required
    @AUDIT.register
    def post(self):
        '''Cria um novo contrato'''
        res = Service.create(API.payload)
        if "form" in res.keys():
            API.abort(400, "Formulário inválido",
                      status=res["form"], statusCode="400")
        return res, 201


@ROLE.register
@API.route('/<int:_id>')
@API.response(404, 'Contrato não encontrado')
@API.param('_id', 'Identificador do contrato')
class ContractItem(Resource):
    '''Exibe um contrato e permite a manipulação do mesmo'''
    @API.doc('get_contract')
    @API.doc(security='jwt')
    # @API.marshal_with(_CONTRACT)
    @API.response(200, 'Contrato apresentado', _CONTRACT)
    @AUTH.role_required
    @AUDIT.register
    def get(self, _id):
        '''Exibe um contrato dado seu identificador'''
        res = Service.read(_id)
        if not res:
            API.abort(400, "Contrato não encontrado",
                      status={"id": _id}, statusCode="404")
        return res

    @API.doc('delete_contract')
    @API.doc(security='jwt')
    @API.response(204, 'Contrato apagado')
    @AUTH.role_required
    @AUDIT.register
    def delete(self, _id):
        '''Apaga um contrato dado seu identificador'''
        res = Service.delete(_id)
        if not res:
            API.abort(400, "Contrato não encontrado",
                      status={"id": _id}, statusCode="404")
        return "Contrato apagado com sucesso!", 204

    @API.doc('update_contract')
    @API.doc(security='jwt')
    @API.expect(_CONTRACT)
    @API.response(200, 'Contrato atualizado', _CONTRACT)
    # @API.marshal_with(_CONTRACT, code=200)
    # @AUTH.role_required
    @AUDIT.register
    def put(self, _id):
        '''Atualiza um contrato dado seu identificador'''
        res = Service.update(_id, API.payload)
        if not res:
            API.abort(400, "Contrato não encontrado",
                      status={"id": _id}, statusCode="404")
        return res


@ROLE.register
@API.route('/page/<int:page>',
           '/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/<string:sort>/limit/<int:per_page>/page/<int:page>')
@API.response(200, 'Contrato listado')
@API.response(404, 'URL inválida')
@API.param('page', 'Numero da página')
@API.param('per_page', 'Quantidade de contratos por página')
@API.param('order_by', 'Atributo de ordenação')
@API.param('sort', 'Tipo da ordenação')
class ContractPaginate(Resource):
    '''Lista os contratos com paginação'''
    @API.doc('list_contracts')
    @API.doc(security='jwt')
    # @API.marshal_list_with(_CONTRACT)
    @AUTH.required
    @AUDIT.register
    @UTIL.marshal_paginate
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista os contratos com paginação'''
        res = Service.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            API.abort(404, "URL inválida",
                      status=res["form"], statusCode="400")
        return res
