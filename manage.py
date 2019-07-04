from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import APP, DB

if __name__ == '__main__':
    MIGRATE = Migrate(APP, DB)
    MANAGER = Manager(APP)
    MANAGER.add_command('db', MigrateCommand)
    MANAGER.run()
