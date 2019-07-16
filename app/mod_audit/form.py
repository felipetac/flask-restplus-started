from app.mod_common.form import RestForm
from .model import Model

class Form(RestForm):

    class Meta:
        model = Model
