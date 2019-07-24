from app.mod_common.form import RestForm
from .model import Bill, Cost

class CostForm(RestForm):

    class Meta:
        model = Cost

class BillForm(RestForm):

    class Meta:
        model = Bill
