from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email
from app.mod_common.form import RestForm


class LoginForm(RestForm):
    email = TextField('Email Address',
                      [Email(),
                       Required(message='E-mail é requerido! preenche-o.')])
    password = PasswordField('Password',
                             [Required(message='Precisa fornecer uma senha.')])
    issuer = TextField('Contract Issuer',
                       [Required(message='Código do emissor é requerido! preenche-o.')])
