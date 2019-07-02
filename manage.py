from flask_script import Manager
from app import app

if __name__ == '__main__':
    MANAGER = Manager(app)
    MANAGER.run()
