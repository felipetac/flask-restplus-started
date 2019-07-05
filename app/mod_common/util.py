from urllib import parse
from functools import wraps
import math
from flask import request
from app import DB, PP as PER_PAGE

def paginate(model):
    def decorator(function):
        def wrapper(*args, **kwargs):
            page = 1
            per_page = PER_PAGE
            if len(args) > 3:
                _cls, apg, appg, _ord_by, _sort = args
                if apg and isinstance(apg, int):
                    page = apg
                if appg and isinstance(appg, int):
                    per_page = appg
            data = function(*args, **kwargs)
            if data:
                count = DB.session.query(model.id).count()
                prev = (page - 1) if page > 1 else None
                last_p = math.ceil(count / per_page)
                nxt = (page + 1) if page < last_p else None
                last_p = last_p if last_p > 0 else 1
                page = {"curr": page, "prev": prev, "next": nxt, "last": last_p}
                return {"data": data, "page": page}
            return data
        return wrapper
    return decorator

def marshal_paginate(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = function(*args, **kwargs)
        if isinstance(data, tuple):
            data = data[0]
        if isinstance(data, dict) and "page" in data.keys():
            for k in ["curr", "prev", "next", "last"]:
                if k in data["page"].keys() and data["page"][k]:
                    data["page"][k] = parse.urljoin(request.base_url, str(data["page"][k]))
        return data
    return wrapper

def get_attributes_class(cls):
    return [i for i in dir(cls) if not callable(i)]
