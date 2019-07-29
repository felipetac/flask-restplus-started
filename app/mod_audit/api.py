from flask_restplus import Namespace, Resource
from app.mod_common.util import Util as UTIL
from app.mod_role.util import Util as ROLE
from app.mod_auth.util import Util as AUTH
from app.mod_auth.api import AUTHORIZATIONS
from .util import Util as AUDIT
from .service import Service


API = Namespace('audit', description='Operações de Auditoria',
                authorizations=AUTHORIZATIONS)


@ROLE.register
@API.route('/page/<int:page>',
           '/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/limit/<int:per_page>/page/<int:page>',
           '/order-by/<string:order_by>/<string:sort>/limit/<int:per_page>/page/<int:page>')
@API.response(200, 'Regra listada')
@API.response(404, 'URL inválida')
@API.param('page', 'Numero da página')
@API.param('per_page', 'Quantidade de ações por página')
@API.param('order_by', 'Atributo de ordenação')
@API.param('sort', 'Tipo da ordenação')
class AuditPaginate(Resource):
    '''Lista as ações com paginação'''
    @API.doc('list_roles')
    @API.doc(security='jwt')
    # @API.marshal_list_with(_ROLE)
    @AUTH.role_required
    @AUDIT.register
    @UTIL.marshal_paginate
    def get(self, page=None, per_page=None, order_by=None, sort=None):
        '''Lista as ações com paginação'''
        res = Service.list(page, per_page, order_by, sort)
        if isinstance(res, dict) and "form" in res.keys():
            API.abort(404, "URL inválida",
                      status=res["form"], statusCode="400")
        return res
