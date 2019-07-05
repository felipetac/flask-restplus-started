from flask_restplus import Resource, fields
from app.mod_user.service import User as UserService
from app.mod_common.util import marshal_paginate
from app import PP as PER_PAGE
from . import API


NS = API.namespace('users', description='Operações da entidade Usuário')

_USER = API.model('User', {
    'id': fields.Integer(readOnly=True, description='Identificador único do usuário'),
    'name': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='E-mail do usuário'),
    'password': fields.String(required=True, description='Senha do usuário')
})

@NS.route('/')
class User(Resource):
    '''Cria um novo usuario'''
    @NS.doc('create_user')
    @NS.expect(_USER)
    @NS.response(201, 'Usuário criado', _USER)
    @NS.response(400, 'Formulário inválido')
    #@NS.marshal_with(_USER, code=201)
    def post(self):
        '''Cria um novo usuário'''
        res = UserService.create(API.payload)
        if "form" in res.keys():
            NS.abort(400, "Formulário inválido", status=res["form"], statusCode="400")
        return res, 201

@NS.route('/<int:_id>')
@NS.response(404, 'Usuário não encontrado')
@NS.param('id', 'Identificador do usuário')
class UserItem(Resource):
    '''Exibe um usuário e permite a manipulação do mesmo'''
    @NS.doc('get_user')
    #@NS.marshal_with(_USER)
    @NS.response(200, 'Usuário apresentado', _USER)
    def get(self, _id):
        '''Exibe um usuário dado seu identificador'''
        res = UserService.read(_id)
        if not res:
            NS.abort(400, "Usuário não encontrado", status={"id": _id}, statusCode="404")
        return res

    @NS.doc('delete_user')
    @NS.response(204, 'Usuário apagado')
    def delete(self, _id):
        '''Apaga um usuário dado seu identificador'''
        res = UserService.delete(_id)
        if not res:
            NS.abort(400, "Usuário não encontrado", status={"id": _id}, statusCode="404")
        return "Usuário apagado com sucesso!", 204

    @NS.doc('update_user')
    @NS.expect(_USER)
    @NS.response(200, 'Usuário atualizado', _USER)
    #@NS.marshal_with(_USER, code=200)
    def put(self, _id):
        '''Atualiza um usuário dado seu identificador'''
        res = UserService.update(_id, API.payload)
        if not res:
            NS.abort(400, "Usuário não encontrado", status={"id": _id}, statusCode="404")
        return res

@NS.route('/page/<int:page>',
          '/limit/<int:per_page>/page/<int:page>',
          '/order-by/<string:order_by>/limit/<int:per_page>/page/<int:page>',
          '/order-by/<string:order_by>/<string:sort>/limit/<int:per_page>/page/<int:page>')
@NS.response(200, 'Usuário listado')
@NS.response(400, 'Formulário inválido')
@NS.param('page', 'Numero da página')
@NS.param('per_page', 'Quantidade de usuários por página')
@NS.param('order_by', 'Atributo de ordenação')
@NS.param('sort', 'Tipo da ordenação')
class UserPaginate(Resource):
    '''Lista os usuários com paginação'''
    @NS.doc('list_users')
    #@NS.marshal_list_with(_USER)
    @marshal_paginate
    def get(self, page, per_page=PER_PAGE, order_by=None, sort="desc"):
        '''Lista os usuários com paginação'''
        res = UserService.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            NS.abort(400, "Formulário inválido", status=res["form"], statusCode="400")
        return res
