"""
系统入口文件，
实例化app
添加shell脚本
"""
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from admins import db, AdminUser
from pictures.models import *
from users.models import Users

app = create_app('dev')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("runserver",
                    Server(host='0.0.0.0',
                           port=5000,
                           ))
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
