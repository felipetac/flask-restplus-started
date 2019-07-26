from app.mod_common.model import DB, BaseModel, BaseSchema

class Model(BaseModel):

    __tablename__ = 'app_contract_owner'

    name = DB.Column(DB.String(200), nullable=False)
    cpf_cnpj = DB.Column(DB.String(50), nullable=False,
                         unique=True, index=True)

class Schema(BaseSchema):

    class Meta:
        model = Model
