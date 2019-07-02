from flask_restplus import Resource, fields
from app.mod_auth.api import API
from app.mod_auth.core.service.user import User as UserService


NS = API.namespace('users', description='User operations')

_USER = API.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'name': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password')
})

@NS.route('/')
class User(Resource):
    '''Shows a list of all users, and lets you POST to add new user'''
    @NS.doc('list_users')
    @NS.marshal_list_with(_USER)
    def get(self):
        '''List all users'''
        return UserService.list()

    @NS.doc('create_user')
    @NS.expect(_USER)
    @NS.marshal_with(_USER, code=201)
    def post(self):
        '''Create a new user'''
        return UserService.create(API.payload), 201

@NS.route('/<int:id>')
@NS.response(404, 'User not found')
@NS.param('id', 'The user identifier')
class UserItem(Resource):
    '''Show a single user item and lets you delete them'''
    @NS.doc('get_user')
    @NS.marshal_with(_USER)
    def get(self, _id):
        '''Fetch a given resource'''
        res = UserService.read(_id)
        if not res:
            return "Usuário não encontrado.", 404
        return res

    @NS.doc('delete_user')
    @NS.response(204, 'User deleted')
    def delete(self, _id):
        '''Delete a user given its identifier'''
        res = UserService.delete(_id)
        if not res:
            return "Usuário não encontrado.", 404
        return "Usuário apagado com sucesso!", 204

    @NS.expect(_USER)
    @NS.marshal_with(_USER)
    def put(self, _id):
        '''Update a user given its identifier'''
        res = UserService.update(_id, API.payload)
        if not res:
            return "Usuário não encontrado.", 404
        return res
