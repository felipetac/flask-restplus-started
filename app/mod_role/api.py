from flask_restplus import Resource, fields
from app.mod_role.service import Role as RoleService
from app.mod_common.util import marshal_paginate
from app.api import API
from .util import Role as ROLE

NS = API.namespace('roles', description='Operações da entidade Regra')

_ROLE = API.model('Role', {
    'id': fields.Integer(readOnly=True, description='Identificador único do regra'),
    'module_name': fields.String(required=True, description='Nome do modulo'),
    'class_name': fields.String(required=True, description='Nome da Classe'),
    'method_name': fields.String(required=True, description='Nome do Método'),
    'role_name': fields.String(required=True, description='Nome da regra'),
    'role_desc': fields.String(required=True, description='Descrição da Regra')
})

@ROLE.register
@NS.route('/')
class Role(Resource):
    '''Cria uma nova regra'''
    @NS.doc('create_role')
    @NS.expect(_ROLE)
    @NS.response(201, 'Regra criada', _ROLE)
    @NS.response(400, 'Formulário inválido')
    #@NS.marshal_with(_ROLE, code=201)
    def post(self):
        '''Cria uma nova regra'''
        res = RoleService.create(API.payload)
        if "form" in res.keys():
            NS.abort(400, "Formulário inválido", status=res["form"], statusCode="400")
        return res, 201

@ROLE.register
@NS.route('/<int:_id>')
@NS.response(404, 'Regra não encontrado')
@NS.param('_id', 'Identificador do regra')
class RoleItem(Resource):
    '''Exibe um regra e permite a manipulação do mesmo'''
    @NS.doc('get_role')
    #@NS.marshal_with(_ROLE)
    @NS.response(200, 'Regra apresentado', _ROLE)
    def get(self, _id):
        '''Exibe um regra dado seu identificador'''
        res = RoleService.read(_id)
        if not res:
            NS.abort(400, "Regra não encontrado", status={"id": _id}, statusCode="404")
        return res

    @NS.doc('delete_role')
    @NS.response(204, 'Regra apagada')
    def delete(self, _id):
        '''Apaga um regra dado seu identificador'''
        res = RoleService.delete(_id)
        if not res:
            NS.abort(400, "Regra não encontrado", status={"id": _id}, statusCode="404")
        return "Regra apagada com sucesso!", 204

    @NS.doc('update_role')
    @NS.expect(_ROLE)
    @NS.response(200, 'Regra atualizada', _ROLE)
    #@NS.marshal_with(_ROLE, code=200)
    def put(self, _id):
        '''Atualiza um regra dado seu identificador'''
        res = RoleService.update(_id, API.payload)
        if not res:
            NS.abort(400, "Regra não encontrado", status={"id": _id}, statusCode="404")
        return res

@ROLE.register
@NS.route('/page/<int:page>',
          '/limit/<int:per_page>/page/<int:page>',
          '/order-by/<string:order_by>/limit/<int:per_page>/page/<int:page>',
          '/order-by/<string:order_by>/<string:sort>/limit/<int:per_page>/page/<int:page>')
@NS.response(200, 'Regra listada')
@NS.response(404, 'URL inválida')
@NS.param('page', 'Numero da página')
@NS.param('per_page', 'Quantidade de regras por página')
@NS.param('order_by', 'Atributo de ordenação')
@NS.param('sort', 'Tipo da ordenação')
class RolePaginate(Resource):
    '''Lista os regras com paginação'''
    @NS.doc('list_roles')
    #@NS.marshal_list_with(_ROLE)
    @marshal_paginate
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista os regras com paginação'''
        res = RoleService.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            NS.abort(404, "URL inválida", status=res["form"], statusCode="400")
        return res
