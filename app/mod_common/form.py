from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
import wtforms_json
from app import DB
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
