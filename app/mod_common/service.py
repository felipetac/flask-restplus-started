from abc import ABC, abstractstaticmethod, abstractclassmethod # Para implementar abstract class
import math
from app import DB, MA, PP as PER_PAGE
from .util import get_attributes_class
from .model import Base as BaseModel
from .form import RestForm

class Base(ABC):

    @classmethod
    def list(cls, page=1, per_page=PER_PAGE, order_by=None, sort=None):
        if not cls.Meta.model or not issubclass(cls.Meta.model, BaseModel):
            raise Exception("É necessário passar o atributo 'model'" +
                            "(Objeto SQLAlchemy) na classe inner Meta")
        if not cls.Meta.schema or not issubclass(cls.Meta.schema, MA.ModelSchema):
            raise Exception("É necessário passar o atributo 'schema'" +
                            "(Objeto Marshmallow) na classe inner Meta")
        if not cls.Meta.form or not issubclass(cls.Meta.form, RestForm):
            raise Exception("É necessário passar o atributo 'form'" +
                            "(Objeto WTForm) na classe inner Meta")
        if page and isinstance(page, int) and \
        per_page and isinstance(per_page, int):
            if not order_by or order_by not in get_attributes_class(cls.Meta.model):
                if not "order_by" in get_attributes_class(cls.Meta) or not cls.Meta.order_by:
                    order_by = getattr(cls.Meta.model, "id")
                else:
                    order_by = getattr(cls.Meta.model, cls.Meta.order_by)
            else:
                order_by = getattr(cls.Meta.model, order_by)
            if not sort or sort not in ["asc", "desc"]:
                if not cls.Meta.sort:
                    raise Exception("Énecessário passar o atributo 'sort' \
                                    ('asc' ou 'desc') na classe inner Meta")
                orderby_and_sort = getattr(order_by, cls.Meta.sort)
            else:
                orderby_and_sort = getattr(order_by, sort)
            entities = cls.Meta.model.query \
                                  .order_by(orderby_and_sort()) \
                                  .paginate(page, per_page, error_out=False).items
            if entities:
                entity_schema = cls.Meta.schema(many=True) # pylint: disable=not-callable
                data = entity_schema.dump(entities)
                if data:
                    count = DB.session.query(order_by).count()
                    prev = (page - 1) if page > 1 else None
                    last_p = math.ceil(count / per_page)
                    nxt = (page + 1) if page < last_p else None
                    last_p = last_p if last_p > 0 else 1
                    page = {"curr": page, "prev": prev, "next": nxt, "last": last_p}
                    return {"data": data, "page": page}
                return data
            return []
        return None

    @classmethod
    def read(cls, entity_id, serializer=True):
        if not cls.Meta.model or not issubclass(cls.Meta.model, BaseModel):
            raise Exception("É necessário passar o atributo 'model'" +
                            "(Objeto SQLAlchemy) na classe inner Meta")
        if not cls.Meta.schema or not issubclass(cls.Meta.schema, MA.ModelSchema):
            raise Exception("É necessário passar o atributo 'schema'" +
                            "(Objeto Marshmallow) na classe inner Meta")
        if entity_id and isinstance(entity_id, int):
            entity = cls.Meta.model.query.filter_by(id=entity_id).first()
            if entity:
                if serializer:
                    entity_schema = cls.Meta.schema() # pylint: disable=not-callable
                    return entity_schema.dump(entity)
                return entity
        return None

    @classmethod
    def delete(cls, entity_id):
        if not cls.Meta.model or not issubclass(cls.Meta.model, BaseModel):
            raise Exception("É necessário passar o atributo 'model'" +
                            "(Objeto SQLAlchemy) na classe inner Meta")
        if entity_id and isinstance(entity_id, int):
            entity = cls.read(entity_id, serializer=False)
            if entity:
                DB.session.delete(entity)
                DB.session.commit()
                return True
        return None

    @abstractstaticmethod
    def create(json_obj):
        pass

    @abstractclassmethod
    def update(cls, user_id, json_obj):
        pass

    class Meta:
        model = None
        schema = None
        form = None
        order_by = "id"
        sort = "desc"
