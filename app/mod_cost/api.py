from flask_restplus import Namespace, Resource, fields
from app.mod_role.service import Service as ROLE
from app.mod_audit.service import Service as AUDIT
from app.mod_auth.service import Service as AUTH
from app.mod_auth.api import AUTHORIZATIONS
from .service import Service as COST

API = Namespace('cost', description='Operações do Custo',
                authorizations=AUTHORIZATIONS)

_COST = API.model('Cost', {
    'role_id': fields.Integer(required=True, description='Id da Regra'),
    'cost': fields.Float(required=True, description='Valor do custo da requisição',
                         example="0.005678")
})


@ROLE.register
@API.route('/')
class Cost(Resource):
    '''Cria um novo custo'''
    @API.doc('create_cost')
    @API.doc(security='jwt')
    @API.expect(_COST)
    @API.response(201, 'Custo criado', _COST)
    @API.response(400, 'Formulário inválido')
    @AUTH.required
    @AUDIT.register
    def post(self):
        '''Cria um novo custo'''
        res = COST.create(API.payload)
        if "form" in res.keys():
            API.abort(400, "Formulário inválido",
                      status=res["form"], statusCode="400")
        return res, 201


@ROLE.register
@API.route('/<int:_id>')
@API.response(404, 'Custo não encontrado')
@API.param('_id', 'Identificador do custo')
class CostItem(Resource):
    '''Exibe um custo e permite a manipulação do mesmo'''
    @API.doc('get_cost')
    @API.doc(security='jwt')
    @API.response(200, 'Custo apresentado', _COST)
    @AUTH.required
    @AUDIT.register
    def get(self, _id):
        '''Exibe um custo dado seu identificador'''
        res = COST.read(_id)
        if not res:
            API.abort(400, "Custo não encontrado",
                      status={"id": _id}, statusCode="404")
        return res

    @API.doc('delete_cost')
    @API.doc(security='jwt')
    @API.response(204, 'Custo apagado')
    @AUTH.required
    @AUDIT.register
    def delete(self, _id):
        '''Apaga um custo dado seu identificador'''
        res = COST.delete(_id)
        if not res:
            API.abort(400, "Custo não encontrado",
                      status={"id": _id}, statusCode="404")
        return "Custo apagado com sucesso!", 204

    @API.doc('update_cost')
    @API.doc(security='jwt')
    @API.expect(_COST)
    @API.response(200, 'Custo atualizado', _COST)
    @AUTH.required
    @AUDIT.register
    def put(self, _id):
        '''Atualiza um custo dado seu identificador'''
        res = COST.update(_id, API.payload)
        if not res:
            API.abort(400, "Custo não encontrado",
                      status={"id": _id}, statusCode="404")
        return res


@ROLE.register
@API.route('/page/<int:page>',
           '/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/<string:sort>/limit/<int:per_page>/page/<int:page>')
@API.response(200, 'Custo listado')
@API.response(404, 'URL inválida')
@API.param('page', 'Numero da página')
@API.param('per_page', 'Quantidade de custos por página')
@API.param('order_by', 'Atributo de ordenação')
@API.param('sort', 'Tipo da ordenação')
class CostPaginate(Resource):
    '''Lista os custos com paginação'''
    @API.doc('list_costs')
    @API.doc(security='jwt')
    @AUTH.required
    @AUDIT.register
    @COST.marshal_paginate
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista os custos com paginação'''
        res = COST.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            API.abort(404, "URL inválida",
                      status=res["form"], statusCode="400")
        return res
