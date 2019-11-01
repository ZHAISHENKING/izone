"""
系统入口文件，
实例化app
添加shell脚本
"""
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from v2.socket_api import socketio
from v1.models import *
app = create_app('dev')
db.create_all(app=app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("runserver",
                    socketio.run(
                        app=app,
                        host='0.0.0.0',
                        port=5000,
                        use_debugger=True
                    ))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
