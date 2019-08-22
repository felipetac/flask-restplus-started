import datetime
from app import DB


class Util(object):

    @staticmethod
    def get_class_attributes(_class):
        return [i for i in dir(_class) if not callable(i) and not i.startswith('_') and
                i not in ["metadata", "query", "query_class"]]

    @staticmethod
    def get_class_methods(_class):
        methods = [func for func in dir(_class) if callable(getattr(_class, func)) and
                   not func.startswith("__")]
        methods = [m for m in methods if m != "Meta"]
        return methods

    @staticmethod
    def model_exists(model_class):
        return model_class.metadata.tables[model_class.__tablename__].exists(DB.engine)

    @staticmethod
    def datetime_delta(delta_sec):
        if delta_sec and isinstance(delta_sec, int):
            return str(datetime.datetime.utcnow() + datetime.timedelta(seconds=delta_sec))
        return None
