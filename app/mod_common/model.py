from app import DB

class Base(DB.Model):

    __abstract__ = True

    id = DB.Column(DB.Integer, primary_key=True)
    date_created = DB.Column(DB.DateTime, default=DB.func.current_timestamp())
    date_modified = DB.Column(DB.DateTime, default=DB.func.current_timestamp(),
                              onupdate=DB.func.current_timestamp())
