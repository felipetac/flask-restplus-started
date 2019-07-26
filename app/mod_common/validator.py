import re
from abc import ABC, abstractstaticmethod
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


class _Validator(ABC): #Python Abstract Class

    def __init__(self, message=None):
        self.message = message if message else "ABC Inválido."

    def __call__(self, form, field):
        if not self.validate(field.data):
            raise ValidationError(self.message)

    @abstractstaticmethod
    def validate(text):
        pass

class CNPJ(_Validator):

    def __init__(self, message=None):
        message = message if message else "CNPJ Inválido."
        super().__init__(self, message)

    @staticmethod
    def validate(text):
        text = ''.join(re.findall(r'\d', str(text)))
        if (not text) or (len(text) < 14):
            return False
        inteiros = list(map(int, text))
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
            return text
        return False

class CPF(_Validator):

    def __init__(self, message=None):
        message = message if message else "CPF Inválido."
        super().__init__(self, message)

    @staticmethod
    def validate(text):
        text = ''.join(re.findall(r'\d', str(text)))
        if (not text) or (len(text) < 11):
            return False
        inteiros = list(map(int, text))
        novo = inteiros[:9]
        while len(novo) < 11:
            # pylint: disable=invalid-name
            r = sum([(len(novo)+1-i)*v for i,v in enumerate(novo)]) % 11
            f = 11 - r if r > 1 else 0
            # pylint: enable=invalid-name
            novo.append(f)
        if novo == inteiros:
            return text
        return False

class CPFCNPJ(_Validator):

    def __init__(self, message=None):
        message = message if message else "CPF ou CNPJ Inválido."
        super().__init__(self, message)

    @staticmethod
    def validate(text):
        text = ''.join(re.findall(r'\d', str(text)))
        if text:
            if len(text) < 11:
                return False
            elif len(text) < 14:
                return CPF.validate(text)
            else:
                return CNPJ.validate(text)
        return False
