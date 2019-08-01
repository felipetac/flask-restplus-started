from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import DB, create_app

if __name__ == '__main__':
    APP = create_app()
    MIGRATE = Migrate(APP, DB)
    MANAGER = Manager(APP)
    MANAGER.add_command('db', MigrateCommand)
    MANAGER.run()
