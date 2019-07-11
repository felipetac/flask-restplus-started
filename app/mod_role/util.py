from .service import Role as RoleService

ROLES_REGISTRY = []

def register_role(cls):
    module_name = cls.__module__
    class_name = cls.__name__
    methods = [func for func in dir(cls) if callable(getattr(cls, func)) and \
                not func.startswith("__")]
    methods = [m for m in methods if m in ["get", "post", "put", "delete"]]
    for method in methods:
        ROLES_REGISTRY.append({"module_name": module_name,
                               "class_name": class_name,
                               "method_name": method,
                               "role_name": class_name+"."+method})
    return cls

def create_all_roles():
    for obj in ROLES_REGISTRY:
        if not RoleService.read_by_attrs(obj["module_name"],
                                         obj["class_name"],
                                         obj["method_name"]):
            RoleService.create(obj)

class Role(object):

    def __init__(self, app):
        self.app = app

    @classmethod
    def register(cls, _class):
        module_name = _class.__module__
        class_name = _class.__name__
        methods = [func for func in dir(_class) if callable(getattr(_class, func)) and \
                    not func.startswith("__")]
        methods = [m for m in methods if m in ["get", "post", "put", "delete"]]
        for method in methods:
            ROLES_REGISTRY.append({"module_name": module_name,
                                   "class_name": class_name,
                                   "method_name": method,
                                   "role_name": class_name+"."+method})
        return _class

    def create_all(self):
        with self.app.app_context():
            for obj in ROLES_REGISTRY:
                if not RoleService.read_by_attrs(obj["module_name"],
                                                 obj["class_name"],
                                                 obj["method_name"]):
                    RoleService.create(obj)
