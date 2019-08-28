from copy import copy
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
import wtforms_json
from werkzeug.datastructures import MultiDict
from wtforms import IntegerField, SelectField, SelectMultipleField
from wtforms.validators import Optional, NumberRange
from wtforms.compat import text_type
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

    # Fix por causa do Swagger UI
    @classmethod
    def from_json(cls, formdata=None, obj=None, prefix='', data=None,
                  meta=None, skip_unknown_keys=True, **kwargs):

        # Fix -----------------------
        form_temp = formdata.copy()
        for key in form_temp.keys():
            if not formdata[key] or formdata[key] == [0]:
                del formdata[key]
        # ---------------------------

        form = cls(
            formdata=MultiDict(
                wtforms_json.flatten_json(
                    cls, formdata, skip_unknown_keys=skip_unknown_keys)
            ) if formdata else None,
            obj=obj,
            prefix=prefix,
            data=data,
            meta=meta,
            **kwargs
        )
        return form

    def load_choices(self):
        pass # função para ser reimplementada para carregar os choices dinâmicos


class ListForm(RestForm):

    page = IntegerField("Número da Página", default=1)
    per_page = IntegerField("Quantidade de itens por página",
                            default=PER_PAGE,
                            validators=[Optional(), NumberRange(min=5, max=PER_PAGE)])
    order_by = SelectField("Ordenar por", validators=[Optional()],
                           default="id")
    sort = SelectField("Ordenar por", validators=[Optional()],
                       choices=[("asc", "asc"), ("desc", "desc")], default="desc")


class SelectModelField(SelectField):
    #pylint: disable=attribute-defined-outside-init

    def __init__(self, model, label=None, validators=None, coerce=text_type, choices=None,
                 **kwargs):
        super().__init__(label, validators, **kwargs)
        self.model = model
        self.coerce = coerce
        self.choices = copy(choices)

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                prk = self.coerce(valuelist[0])
                entity = self.model.query.filter_by(id=prk).first()
                self.data = entity
            except ValueError:
                raise ValueError(self.gettext(
                    'Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        for value, _ in self.choices:
            if self.data.id == value:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))

    #pylint: enable=attribute-defined-outside-init


class SelectMultipleModelField(SelectMultipleField):

    def __init__(self, model, label=None, validators=None, coerce=text_type, choices=None,
                 **kwargs):
        super().__init__(label, validators, **kwargs)
        self.model = model
        self.coerce = coerce
        self.choices = copy(choices)

    def process_formdata(self, valuelist):
        try:
            model = self.model()
            models = []
            ids = list(self.coerce(x) for x in valuelist)
            for idd in ids:
                ret = model.query.filter_by(id=idd).first()
                if ret:
                    models.append(ret)
            self.data = models  # pylint: disable=attribute-defined-outside-init
        except ValueError:
            raise ValueError(
                self.gettext('Invalid choice(s): one or more data inputs could not be coerced'))

    def pre_validate(self, form):
        if self.data:
            values = list(c[0] for c in self.choices)
            for data in self.data:
                if data.id not in values:
                    raise ValueError(self.gettext(
                        "'%(value)s' is not a valid choice for this field") % dict(value=data.id))
