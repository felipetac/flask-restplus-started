from app.mod_common.model import DB, BaseModel, BaseSchema

class Model(BaseModel):

    __tablename__ = 'app_service'

    module_name = DB.Column(DB.String(200), nullable=False)
    class_name = DB.Column(DB.String(200), nullable=False)
    method_name = DB.Column(DB.String(200), nullable=False)

    __table_args__ = (DB.UniqueConstraint('module_name', 'class_name',
                                          'method_name', name='_unique_service'),)

class Schema(BaseSchema):

    class Meta:
        model = Model
