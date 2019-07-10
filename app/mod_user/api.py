from flask_restplus import Namespace, Resource, fields
from app.mod_user.service import User as UserService
from app.mod_common.util import marshal_paginate
from app.mod_role.util import register_role

API = Namespace('users', description='Operações da entidade Usuário')

_USER = API.model('User', {
    'id': fields.Integer(readOnly=True, description='Identificador único do usuário'),
    'name': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='E-mail do usuário'),
    'password': fields.String(required=True, description='Senha do usuário'),
    'roles_id': fields.List(fields.Integer(required=False, description='Lista de ids das regras'))
})

@register_role
@API.route('/')
class User(Resource):
    '''Cria um novo usuario'''
    @API.doc('create_user')
    @API.expect(_USER)
    @API.response(201, 'Usuário criado', _USER)
    @API.response(400, 'Formulário inválido')
    #@API.marshal_with(_USER, code=201)
    def post(self):
        '''Cria um novo usuário'''
        res = UserService.create(API.payload)
        if "form" in res.keys():
            API.abort(400, "Formulário inválido", status=res["form"], statusCode="400")
        return res, 201

@register_role
@API.route('/<int:_id>')
@API.response(404, 'Usuário não encontrado')
@API.param('_id', 'Identificador do usuário')
class UserItem(Resource):
    '''Exibe um usuário e permite a manipulação do mesmo'''
    @API.doc('get_user')
    #@API.marshal_with(_USER)
    @API.response(200, 'Usuário apresentado', _USER)
    def get(self, _id):
        '''Exibe um usuário dado seu identificador'''
        res = UserService.read(_id)
        if not res:
            API.abort(400, "Usuário não encontrado", status={"id": _id}, statusCode="404")
        return res

    @API.doc('delete_user')
    @API.response(204, 'Usuário apagado')
    def delete(self, _id):
        '''Apaga um usuário dado seu identificador'''
        res = UserService.delete(_id)
        if not res:
            API.abort(400, "Usuário não encontrado", status={"id": _id}, statusCode="404")
        return "Usuário apagado com sucesso!", 204

    @API.doc('update_user')
    @API.expect(_USER)
    @API.response(200, 'Usuário atualizado', _USER)
    #@API.marshal_with(_USER, code=200)
    def put(self, _id):
        '''Atualiza um usuário dado seu identificador'''
        res = UserService.update(_id, API.payload)
        if not res:
            API.abort(400, "Usuário não encontrado", status={"id": _id}, statusCode="404")
        return res

@register_role
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
    #@API.marshal_list_with(_USER)
    @marshal_paginate
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista os usuários com paginação'''
        res = UserService.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            API.abort(404, "URL inválida", status=res["form"], statusCode="400")
        return res
