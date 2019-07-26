from app.mod_common.form import RestForm
from app.mod_common.validator import CPFCNPJ
from .model import Model


class Form(RestForm):

    class Meta:
        model = Model
        field_args = {'cpf_cnpj': {'validators': [CPFCNPJ]}}
