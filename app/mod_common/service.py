# from abc import ABC #, abstractstaticmethod, abstractclassmethod # Para implementar abstract class
import math
from urllib import parse
from functools import wraps
from flask import request
from .util import Util
from .model import DB, BaseModel, BaseSchema
from .form import RestForm, ListForm


class BaseService():

    class Meta:
        model = BaseModel
        schema = BaseSchema
        form = RestForm
        order_by = "id"
        sort = "desc"

    @classmethod
    def list(cls, page=None, per_page=None, order_by=None, sort=None):
        cls._validate_instances(["model", "form", "schema"])
        obj = {}
        for attr in ["page", "per_page", "order_by", "sort"]:
            _attr = eval(attr)  # pylint: disable=eval-used
            if _attr:
                obj[attr] = _attr
        form = ListForm.from_json(obj)
        form.order_by.choices = [
            (i, i) for i in Util.get_class_attributes(cls.Meta.model)]
        if form.validate():
            page, per_page, order_by, sort = form.page.data, form.per_page.data, \
                form.order_by.data, form.sort.data
            order_by = getattr(cls.Meta.model, order_by)
            orderby_and_sort = getattr(order_by, sort)
            entities = cls.Meta.model.query \
                .order_by(orderby_and_sort()) \
                .paginate(page, per_page, error_out=False).items
            if entities:
                entity_schema = cls.Meta.schema(
                    many=True)  # pylint: disable=not-callable
                data = entity_schema.dump(entities)
                if data:
                    count = DB.session.query(order_by).count()
                    prev = (page - 1) if page > 1 else None
                    last_p = math.ceil(count / per_page)
                    nxt = (page + 1) if page < last_p else None
                    last_p = last_p if last_p > 0 else 1
                    page = {"curr": page, "prev": prev,
                            "next": nxt, "last": last_p}
                    return {"data": data, "page": page}
                return data
            return []
        return {"form": form.errors}

    @classmethod
    def read(cls, entity_id, serialize=True):
        cls._validate_instances(["model", "schema"])
        if entity_id and isinstance(entity_id, int):
            entity = cls.Meta.model.query.filter_by(id=entity_id).first()
            if entity:
                if serialize:
                    entity_schema = cls.Meta.schema()  # pylint: disable=not-callable
                    return entity_schema.dump(entity)
                return entity
        return None

    @classmethod
    def delete(cls, entity_id):
        cls._validate_instances(["model"])
        if entity_id and isinstance(entity_id, int):
            entity = cls.read(entity_id, serialize=False)
            if entity:
                DB.session.delete(entity)
                DB.session.commit()
                return True
        return None

    @classmethod
    def create(cls, json_obj, serialize=True):
        cls._validate_instances(["model", "form", "schema"])
        form = cls.Meta.form.from_json(json_obj)
        if form.validate():
            model = cls.Meta.model()
            form.populate_obj(model)
            DB.session.add(model)
            DB.session.commit()
            if serialize:
                schema = cls.Meta.schema()
                return schema.dump(model)
            return model
        return {"form": form.errors}

    @classmethod
    def update(cls, entity_id, json_obj, serialize=True):
        cls._validate_instances(["form", "schema"])
        if entity_id and isinstance(entity_id, int):
            obj = cls.read(entity_id, serialize=False)
            if obj:
                form = cls.Meta.form.from_json(json_obj, obj=obj)
                if form.validate_on_submit():
                    form.populate_obj(obj)
                    DB.session.commit()
                    if serialize:
                        schema = cls.Meta.schema()
                        return schema.dump(obj)
                    return obj
                return {"form": form.errors}
        return None

    @classmethod
    def truncate(cls):
        cls.Meta.model.query.delete()

    @classmethod
    def get_choices(cls, column_key_name, column_value_name):
        cls._validate_instances(["model"])
        model = cls.Meta.model
        if Util.model_exists(model):
            return model.query.with_entities(getattr(model, column_key_name),
                                             getattr(model, column_value_name)).all()
        return []

    @classmethod
    def _validate_instances(cls, instances=None):
        if instances and isinstance(instances, list):
            for instance in instances:
                if instance == "model":
                    if isinstance(cls.Meta.model, BaseModel) or \
                       not issubclass(cls.Meta.model, BaseModel):
                        raise Exception("É necessário passar o atributo 'model'" +
                                        "(Objeto SQLAlchemy) na classe inner Meta")
                if instance == "schema":
                    if isinstance(cls.Meta.schema, BaseSchema) or \
                       not issubclass(cls.Meta.schema, BaseSchema):
                        raise Exception("É necessário passar o atributo 'schema'" +
                                        "(Objeto Marshmallow) na classe inner Meta")
                if instance == "form":
                    if isinstance(cls.Meta.form, RestForm) or \
                       not issubclass(cls.Meta.form, RestForm):
                        raise Exception("É necessário passar o atributo 'form'" +
                                        "(Objeto WTForm) na classe inner Meta")

    @staticmethod
    def marshal_paginate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            data = function(*args, **kwargs)
            if isinstance(data, tuple):
                data = data[0]
            if isinstance(data, dict) and "page" in data.keys():
                for k in ["curr", "prev", "next", "last"]:
                    if k in data["page"].keys() and data["page"][k]:
                        data["page"][k] = parse.urljoin(
                            request.base_url, str(data["page"][k]))
            return data
        return wrapper
