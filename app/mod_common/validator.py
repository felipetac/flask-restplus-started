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
