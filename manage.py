"""
    Created by zltningx on 18-4-28.
"""

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import Admin, Plugin

import os


app = create_app(os.environ.get("CONFIG_NAME") or 'development')
manage = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Admin=Admin, Plugin=Plugin)


manage.add_command("shell", Shell(make_context=make_shell_context))
manage.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manage.run()