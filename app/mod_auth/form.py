from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, Length, Optional
from app.mod_common.form import RestForm
from .validator import Key, Password, EmailExists, Issuer


class LoginForm(RestForm):
    email = TextField('Email Address',
                      [Email(), Required(message='E-mail é requerido.'),
                       EmailExists()])
    password = PasswordField('Password',
                             [Required(message='Senha é requerida.'),
                              Length(min=6, max=12), Password()])
    issuer = TextField('Contract Issuer',
                       [Required(message='Código do emissor é requerido.'), Issuer()])


class KeyForm(RestForm):
    key = TextField('JWT Key', [Required(message='A chave JWT é requerida.'), Key()])
    issuer = TextField('Contract Issuer', [Optional(), Issuer()])
