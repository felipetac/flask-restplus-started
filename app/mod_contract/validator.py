from wtforms import ValidationError
from wtforms_alchemy import Unique as Uq


class UniqueRolePerCNPJ(Uq):

    def __call__(self, form, field):
        columns = self._syntaxes_as_tuples(form, field, self.column)
        self.model = columns[0][1].class_  # pylint: disable=attribute-defined-outside-init
        roles_ids = form.roles_id.data
        owner_id = form.owner_id.data
        contracts = self.query.filter(
            self.model.owner_id == owner_id).all()
        cnpj_roles_lsts = [[r.id for r in c.roles] for c in contracts]
        roles_joined = []
        for lst in cnpj_roles_lsts:
            roles_joined += lst
        roles_joined = set(roles_joined)
        for role in roles_joined:
            for c_role in roles_ids:
                if c_role == role:
                    self.message = "O id '%d' já está cadastrado para o CNPJ." % c_role
                    raise ValidationError(self.message)
