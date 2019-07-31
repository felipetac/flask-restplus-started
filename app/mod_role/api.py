from flask_restplus import Namespace, Resource
from app.mod_auth.service import Service as AUTH
from app.mod_auth.api import AUTHORIZATIONS
from app.mod_audit.service import Service as AUDIT
from .service import Service as ROLE

API = Namespace('role', description='Operações da Regra', authorizations=AUTHORIZATIONS)

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
    @API.doc(security='jwt')
    #@API.marshal_list_with(_ROLE)
    @AUTH.required
    @ROLE.marshal_paginate
    @AUDIT.register
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista os regras com paginação'''
        res = ROLE.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            API.abort(404, "URL inválida", status=res["form"], statusCode="400")
        return res
