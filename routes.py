"""
蓝图、全局路由实例化
"""

from admins import Index, LogoutView, LoginView
from flask import Blueprint
from flask_restful import Api
from pictures.api import *
from files.api import *

# 实例化蓝图,路由前缀为/docs
blue = Blueprint('api', __name__, url_prefix='/api')

docs = Api(blue)


docs.add_resource(Index, '/', endpoint="index")
docs.add_resource(LogoutView, '/logout/', endpoint="logout")
docs.add_resource(LoginView, '/login/', endpoint="login")

docs.add_resource(Upload, '/upload/')
docs.add_resource(GetAllImage, '/image/all/')
docs.add_resource(GetAllCategory, '/category/all/')
docs.add_resource(GetPic, '/image/')
docs.add_resource(VideoUpload, '/up_video/')
docs.add_resource(GetAllVideo, '/video/all/')


