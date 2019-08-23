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
    issuer = TextField('Account Code',
                       [Required(message='Código do emissor do token é requerido.'), Issuer()])


class KeyForm(RestForm):
    key = TextField('JWT Key', [Required(message='A token é requerido.'), Key()])
    issuer = TextField('Account Code', [Optional(), Issuer()])
