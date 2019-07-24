from flask_restplus import Namespace, Resource
from app.mod_common.util import Util as UTIL
from app.mod_auth.util import Util as AUTH
from app.mod_auth.api import AUTHORIZATIONS
from app.mod_audit.util import Util as AUDIT
from app.mod_role.util import Util as ROLE
from .service import BillService

API = Namespace('billing', description='Operações de Bilhetagem', authorizations=AUTHORIZATIONS)

@ROLE.register
@API.route('/service/page/<int:page>',
           '/service/limit/<int:per_page>/page/<int:page>',
           '/service/order-by/<string:order_by>/limit/<int:per_page>/page/<int:page>',
           '/service/order-by/<string:order_by>/<string:sort>/limit/<int:per_page>/page/<int:page>')
@API.response(200, 'Regra listada')
@API.response(404, 'URL inválida')
@API.param('page', 'Numero da página')
@API.param('per_page', 'Quantidade de regras por página')
@API.param('order_by', 'Atributo de ordenação')
@API.param('sort', 'Tipo da ordenação')
class ServicePaginate(Resource):
    '''Lista os serviços com paginação'''
    @API.doc('list_services')
    @API.doc(security='jwt')
    #@API.marshal_list_with(_ROLE)
    @AUTH.role_required
    @UTIL.marshal_paginate
    @AUDIT.register
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista os serviços com paginação'''
        res = BillService.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            API.abort(404, "URL inválida", status=res["form"], statusCode="400")
        return res
