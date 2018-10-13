"""
将应用在此注册
flask-login
mongoengine
BluePrint
Sentry
logging
CORS
babel
"""

from flask import Flask, request, render_template
from flask_cors import CORS
from routes import docs
from werkzeug.utils import import_string
from config import config
from admins import admin, login, AdminUser, db, ModelView
from flask_babelex import Babel
import logging
from pictures.view import *
from users.view import *
from files.view import *
from flask_admin.contrib.fileadmin import FileAdmin


# models引用必须在 login_manager之后，不然会循环引用
blueprints = ['routes:blue']

# model视图注册
admin.add_view(PicView(name=u"图片"))
admin.add_view(ModelView(Category, db.session, name="分类"))
admin.add_view(VideoView(name="视频"))
admin.add_view(FileAdmin('/data/upload/', name=u"文件"))
admin.add_view(MyUserlView(name=u"用户"))


# 初始化app
def create_app(config_name):
    app = Flask(config_name)
    app.config.from_object(config[config_name])

    # 全局响应头
    @app.after_request
    def after_request(response):
        if "Access-Control-Allow-Origin" not in response.headers.keys():
            response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    # flask-login初始化
    def init_login():
        login_manager = login.LoginManager()
        login_manager.setup_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return db.session.query(AdminUser).get(user_id)

    # 日志配置
    handler = logging.FileHandler('app.log', encoding='UTF-8')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)

    # 应用注册
    app.logger.addHandler(handler)
    db.init_app(app)
    admin.init_app(app)
    docs.init_app(app)
    config[config_name].init_app(app)
    babel = Babel(app)
    init_login()

    # 注册所有蓝图
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return render_template('index.html')
    # 跨域
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
    return app
