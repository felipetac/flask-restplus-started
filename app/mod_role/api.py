from flask_restplus import Namespace, Resource, fields
from app.mod_common.util import Util as UTIL
from app.mod_auth.util import Util as AUTH
from app.mod_audit.util import Util as AUDIT
from .service import Service
from .util import Util as ROLE

API = Namespace('roles', description='Operações da entidade Regra')

_ROLE = API.model('Role', {
    'id': fields.Integer(readOnly=True, description='Identificador único do regra'),
    'module_name': fields.String(required=True, description='Nome do modulo'),
    'class_name': fields.String(required=True, description='Nome da Classe'),
    'method_name': fields.String(required=True, description='Nome do Método'),
    'role_name': fields.String(required=True, description='Nome da regra'),
    'role_desc': fields.String(required=True, description='Descrição da Regra')
})

@ROLE.register
@API.route('/')
class Role(Resource):
    '''Cria uma nova regra'''
    @API.doc('create_role')
    @API.expect(_ROLE)
    @API.response(201, 'Regra criada', _ROLE)
    @API.response(400, 'Formulário inválido')
    #@API.marshal_with(_ROLE, code=201)
    def post(self):
        '''Cria uma nova regra'''
        res = Service.create(API.payload)
        if "form" in res.keys():
            API.abort(400, "Formulário inválido", status=res["form"], statusCode="400")
        return res, 201

@ROLE.register
@API.route('/<int:_id>')
@API.response(404, 'Regra não encontrado')
@API.param('_id', 'Identificador do regra')
class RoleItem(Resource):
    '''Exibe um regra e permite a manipulação do mesmo'''
    @API.doc('get_role')
    #@API.marshal_with(_ROLE)
    @API.response(200, 'Regra apresentado', _ROLE)
    @AUDIT.register
    def get(self, _id):
        '''Exibe um regra dado seu identificador'''
        res = Service.read(_id)
        if not res:
            API.abort(400, "Regra não encontrado", status={"id": _id}, statusCode="404")
        return res

    @API.doc('delete_role')
    @API.response(204, 'Regra apagada')
    def delete(self, _id):
        '''Apaga um regra dado seu identificador'''
        res = Service.delete(_id)
        if not res:
            API.abort(400, "Regra não encontrado", status={"id": _id}, statusCode="404")
        return "Regra apagada com sucesso!", 204

    @API.doc('update_role')
    @API.expect(_ROLE)
    @API.response(200, 'Regra atualizada', _ROLE)
    #@API.marshal_with(_ROLE, code=200)
    def put(self, _id):
        '''Atualiza um regra dado seu identificador'''
        res = Service.update(_id, API.payload)
        if not res:
            API.abort(400, "Regra não encontrado", status={"id": _id}, statusCode="404")
        return res

@ROLE.register
@API.route('/page/<int:page>',
           '/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/<string:sort>/limit/<int:per_page>/page/<int:page>')
@API.response(200, 'Regra listada')
@API.response(404, 'URL inválida')
@API.param('page', 'Numero da página')
@API.param('per_page', 'Quantidade de regras por página')
@API.param('order_by', 'Atributo de ordenação')
@API.param('sort', 'Tipo da ordenação')
class RolePaginate(Resource):
    '''Lista os regras com paginação'''
    @API.doc('list_roles')
    #@API.marshal_list_with(_ROLE)
    @UTIL.marshal_paginate
    @AUTH.role_required
    @AUDIT.register
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista os regras com paginação'''
        res = Service.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            API.abort(404, "URL inválida", status=res["form"], statusCode="400")
        return res
