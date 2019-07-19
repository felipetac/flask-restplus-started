#from app.mod_common.sanitizer import to_lower
from app.mod_common.form import RestForm
from .model import Model

class Form(RestForm):

    class Meta:
        model = Model
        #field_args = {'role_name': {'filters': [to_lower]}}
