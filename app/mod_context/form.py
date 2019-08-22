import random
from wtforms.fields import SelectMultipleField
from app.mod_common.form import RestForm
from app.mod_contract.service import Service as ContractService
from .model import Model

class Form(RestForm):

    class Meta:
        model = Model

    context_ids = SelectMultipleField(
        'Context Item Ids', choices=ContractService.get_contract_role_choices(), coerce=int)

    def populate_obj(self, entity):
        if self.name.data:
            entity.name = self.name.data
        if self.description.data:
            entity.description = self.description.data
        if self.key_exp.data:
            entity.key_exp = self.key_exp.data
        if not entity.issuer.data:
            entity.issuer = self._create_issuer_name()
        if self.contexts_id.data:
            for context_id in self.contexts_id.data:
                if context_id not in [context.id for context in entity.contexts]:
                    association = ContractService.read_contract_role(context_id)
                    if association:
                        entity.contexts.append(association)

    @classmethod
    def _create_issuer_name(cls):
        from .service import Service # Inner Import para evitar import cíclico
        _hash = random.getrandbits(16)
        issuer = "app-%s" % _hash
        if not Service.read_by_issuer(issuer):
            return issuer
        return cls._create_issuer_name()
