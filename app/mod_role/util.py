from .service import Role as RoleService

ROLES_REGISTRY = []

def register_roles():
    def wrapper(cls):
        module_name = cls.__module__
        class_name = cls.__name__
        methods = __get_class_methods(cls)
        for method in methods:
            ROLES_REGISTRY.append({"module_name": module_name,
                                   "class_name": class_name,
                                   "method_name": method,
                                   "role_name": class_name+"."+method})
    return wrapper

def __get_class_methods(cls):
    methods = [func for func in dir(cls) if callable(getattr(cls, func)) and \
               not func.startswith("__")]
    return [m for m in methods if m in ["get", "post", "put", "delete"]]

def create_all_roles():
    for obj in ROLES_REGISTRY:
        if not RoleService.read_by_attrs(obj["module_name"],
                                         obj["class_name"],
                                         obj["method_name"]):
            RoleService.create(obj)
