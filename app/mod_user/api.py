from flask_restplus import Namespace, Resource, fields
from app.mod_common.util import Util as UTIL
from app.mod_role.util import Util as ROLE
from app.mod_audit.util import Util as AUDIT
from app.mod_auth.util import Util as AUTH
from app.mod_auth.api import AUTHORIZATIONS
from .service import Service

API = Namespace('users', description='Operações do Usuário', authorizations=AUTHORIZATIONS)

_USER = API.model('User', {
    'name': fields.String(required=True, description='Nome do usuário',
                          example="Felipe Toscano"),
    'email': fields.String(required=True, description='E-mail do usuário',
                           example="felipe.toscano@gmail.com"),
    'password': fields.String(required=True, description='Senha do usuário', example="123456"),
    'active': fields.Boolean(required=True, description='Usuario Ativo',
                             example=True),
    'roles_id': fields.List(fields.Integer(required=False, description='Lista de ids das regras'))
})

@ROLE.register
@API.route('/')
class User(Resource):
    '''Cria um novo usuario'''
    @API.doc('create_user')
    #@API.doc(security='jwt')
    @API.expect(_USER)
    @API.response(201, 'Usuário criado', _USER)
    @API.response(400, 'Formulário inválido')
    #@API.marshal_with(_USER, code=201)
    #@AUTH.role_required
    @AUDIT.register
    def post(self):
        '''Cria um novo usuário'''
        res = Service.create(API.payload)
        if "form" in res.keys():
            API.abort(400, "Formulário inválido", status=res["form"], statusCode="400")
        return res, 201

@ROLE.register
@API.route('/<int:_id>')
@API.response(404, 'Usuário não encontrado')
@API.param('_id', 'Identificador do usuário')
class UserItem(Resource):
    '''Exibe um usuário e permite a manipulação do mesmo'''
    @API.doc('get_user')
    @API.doc(security='jwt')
    #@API.marshal_with(_USER)
    @API.response(200, 'Usuário apresentado', _USER)
    @AUTH.role_required
    @AUDIT.register
    def get(self, _id):
        '''Exibe um usuário dado seu identificador'''
        res = Service.read(_id)
        if not res:
            API.abort(400, "Usuário não encontrado", status={"id": _id}, statusCode="404")
        return res

    @API.doc('delete_user')
    @API.doc(security='jwt')
    @API.response(204, 'Usuário apagado')
    @AUTH.role_required
    @AUDIT.register
    def delete(self, _id):
        '''Apaga um usuário dado seu identificador'''
        res = Service.delete(_id)
        if not res:
            API.abort(400, "Usuário não encontrado", status={"id": _id}, statusCode="404")
        return "Usuário apagado com sucesso!", 204

    @API.doc('update_user')
    @API.doc(security='jwt')
    @API.expect(_USER)
    @API.response(200, 'Usuário atualizado', _USER)
    #@API.marshal_with(_USER, code=200)
    @AUTH.role_required
    @AUDIT.register
    def put(self, _id):
        '''Atualiza um usuário dado seu identificador'''
        res = Service.update(_id, API.payload)
        if not res:
            API.abort(400, "Usuário não encontrado", status={"id": _id}, statusCode="404")
        return res

@ROLE.register
@API.route('/page/<int:page>',
           '/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/<string:sort>/limit/<int:per_page>/page/<int:page>')
@API.response(200, 'Usuário listado')
@API.response(404, 'URL inválida')
@API.param('page', 'Numero da página')
@API.param('per_page', 'Quantidade de usuários por página')
@API.param('order_by', 'Atributo de ordenação')
@API.param('sort', 'Tipo da ordenação')
class UserPaginate(Resource):
    '''Lista os usuários com paginação'''
    @API.doc('list_users')
    @API.doc(security='jwt')
    #@API.marshal_list_with(_USER)
    @AUTH.required
    @AUDIT.register
    @UTIL.marshal_paginate
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista os usuários com paginação'''
        res = Service.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            API.abort(404, "URL inválida", status=res["form"], statusCode="400")
        return res
