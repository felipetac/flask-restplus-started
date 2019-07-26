from app.mod_common.service import BaseService
from .model import Bill, Cost, BillSchema, CostSchema
from .form import BillForm, CostForm


class CostService(BaseService):

    class Meta:
        model = Cost
        form = CostForm
        schema = CostSchema


class BillService(BaseService):

    class Meta:
        model = Bill
        form = BillForm
        schema = BillSchema
