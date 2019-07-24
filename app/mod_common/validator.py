import re
from wtforms import ValidationError
from wtforms_components import Email as Em
from wtforms_alchemy import Unique as Uq

 # Customizei estes validadores pois wtforms-alchemy não estava traduzindo
 # https://wtforms-alchemy.readthedocs.io/en/latest/validators.html#overriding-default-validators

class Email(Em):
    def __init__(self, message='Email Inválido.'):
        Em.__init__(self, message=message)

class Unique(Uq):
    def __init__(self, column, get_session=None, message='Já Existe.'):
        Uq.__init__(self, column, get_session=get_session, message=message)

class CNPJ(object):

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not self._validate(field.data):
            if self.message is None:
                self.message = "CPNJ Inválido."
            raise ValidationError(self.message)

    @staticmethod
    def _validate(cnpj):
        cnpj = ''.join(re.findall(r'\d', str(cnpj)))
        if (not cnpj) or (len(cnpj) < 14):
            return False
        inteiros = list(map(int, cnpj))
        novo = inteiros[:12]
        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(novo) < 14:
            # pylint: disable=invalid-name
            r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
            f = 11 - r if r > 1 else 0
            # pylint: enable=invalid-name
            novo.append(f)
            prod.insert(0, 6)
        if novo == inteiros:
            return cnpj
        return False