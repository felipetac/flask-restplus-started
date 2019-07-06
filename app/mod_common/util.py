from urllib import parse
from functools import wraps
import math
from flask import request
from app import DB, PP as PER_PAGE

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
