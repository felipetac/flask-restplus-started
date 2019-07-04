from app import DB

def paginate(model):
    def decorator(function):
        def wrapper(*args, **kwargs):
            page = kwargs["page"] if "page" in kwargs.keys() else 1
            per_page = kwargs["per_page"] if "per_page" in kwargs.keys() else 50
            data = function(*args, **kwargs)
            if data:
                count = DB.session.query(model.id).count()
                prev = (page - 1) if page > 1 else None
                last_p = int(count / per_page)
                nxt = (page + 1) if page < last_p else None
                last_p = last_p if last_p > 0 else 1
                page = {"curr": page, "prev": prev, "next": nxt, "last": last_p}
                return {"data": data, "page": page}
            return data
        return wrapper
    return decorator
