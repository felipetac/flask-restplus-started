from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from wtforms import IntegerField
from wtforms.validators import NumberRange, Optional
import wtforms_json
from app import DB, PP as PER_PAGE
from app.mod_common.validator import Unique, Email

wtforms_json.init()

_BMF = model_form_factory(FlaskForm)

class RestForm(_BMF):

    class Meta:
        csrf = False
        email_validator = Email
        unique_validator = Unique

    @classmethod
    def get_session(cls):
        return DB.session

class PageForm(RestForm):

    per_page = IntegerField('Quantidade de Itens por Página',
                            validators=[Optional(), NumberRange(min=10, max=PER_PAGE)],
                            default=PER_PAGE)
