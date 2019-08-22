from flask import Blueprint
from flask_restplus import Api
from app.mod_user.api import API as UserNS
from app.mod_role.api import API as RoleNS
from app.mod_auth.api import API as AuthNS
from app.mod_audit.api import API as AuditNS
from app.mod_owner.api import API as OwnerNS
from app.mod_contract.api import API as ContractNS
from app.mod_cost.api import API as CostNS
from app.mod_billing.api import API as BillingNS
from app.mod_context.api import API as ContextNS

BLUEPRINT = Blueprint('user_api', __name__, url_prefix='/api/1')

API = Api(BLUEPRINT,
          version='0.1',
          title='API da Aplicação',
          description='API geral da aplicação',)

# Adicionando as rotas dos modulos
API.add_namespace(UserNS)
API.add_namespace(RoleNS)
API.add_namespace(AuthNS)
API.add_namespace(AuditNS)
API.add_namespace(OwnerNS)
API.add_namespace(ContractNS)
API.add_namespace(CostNS)
API.add_namespace(BillingNS)
API.add_namespace(ContextNS)
