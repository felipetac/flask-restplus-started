from abc import ABC, abstractstaticmethod, abstractclassmethod # Para implementar abstract class
import math
from app import DB, MA
from .util import get_attributes_class
from .model import Base as BaseModel
from .form import RestForm, ListForm

class Base(ABC):

    @classmethod
    def list(cls, page=None, per_page=None, order_by=None, sort=None):
        if not cls.Meta.model or not issubclass(cls.Meta.model, BaseModel):
            raise Exception("É necessário passar o atributo 'model'" +
                            "(Objeto SQLAlchemy) na classe inner Meta")
        if not cls.Meta.schema or not issubclass(cls.Meta.schema, MA.ModelSchema):
            raise Exception("É necessário passar o atributo 'schema'" +
                            "(Objeto Marshmallow) na classe inner Meta")
        if not cls.Meta.form or not issubclass(cls.Meta.form, RestForm):
            raise Exception("É necessário passar o atributo 'form'" +
                            "(Objeto WTForm) na classe inner Meta")
        obj = {}
        for attr in ["page", "per_page", "order_by", "sort"]:
            _attr = eval(attr) # pylint: disable=eval-used
            if _attr:
                obj[attr] = _attr
        form = ListForm.from_json(obj)
        form.order_by.choices = [(i, i) for i in get_attributes_class(cls.Meta.model)]
        if form.validate():
            page, per_page = form.page.data, form.per_page.data
            order_by = getattr(cls.Meta.model, form.order_by.data)
            orderby_and_sort = getattr(order_by, form.sort.data)
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
        return {"form": form.errors}

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
    def update(cls, entity_id, json_obj):
        pass

    class Meta:
        model = None
        schema = None
        form = None
        order_by = None
        sort = "desc"
