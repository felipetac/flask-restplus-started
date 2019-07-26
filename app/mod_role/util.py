from .service import Service

_ROLES_REGISTRY = []


class Util(object):

    def __init__(self, app):
        self.app = app

    @classmethod
    def register(cls, _class):
        module_name = _class.__module__
        class_name = _class.__name__
        methods = [func for func in dir(_class) if callable(getattr(_class, func)) and
                   not func.startswith("__")]
        methods = [m for m in methods if m in ["get", "post", "put", "delete"]]
        for method in methods:
            _ROLES_REGISTRY.append({"module_name": module_name,
                                    "class_name": class_name,
                                    "method_name": method,
                                    "name": class_name+"."+method})
        return _class

    def create_all(self):
        roles = []
        with self.app.app_context():
            Service.truncate()
            for obj in _ROLES_REGISTRY:
                roles.append(Service.create(obj))
        return roles
