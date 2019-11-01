"""
系统入口文件，
实例化app
添加shell脚本
"""
from flask_script import Manager
from app import create_app
from v2.socket_api import socketio
from v1.models import *
app = create_app('dev')
db.create_all(app=app)
manager = Manager(app)
manager.add_command("runserver",
                    socketio.run(
                        app=app,
                        host='0.0.0.0',
                        port=5000,
                        use_debugger=False
                    ))

if __name__ == '__main__':
    manager.run()
