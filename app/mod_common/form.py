from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
import wtforms_json
from wtforms import IntegerField, SelectField
from wtforms.validators import Optional, NumberRange
from app import DB, PP as PER_PAGE
from .validator import Unique, Email

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

class ListForm(RestForm):

    page = IntegerField("Número da Página", default=1)
    per_page = IntegerField("Quantidade de itens por página",
                            default=PER_PAGE,
                            validators=[Optional(), NumberRange(min=5, max=PER_PAGE)])
    order_by = SelectField("Ordenar por", validators=[Optional()],
                           default="id")
    sort = SelectField("Ordenar por", validators=[Optional()],
                       choices=[("asc", "asc"), ("desc", "desc")], default="desc")
