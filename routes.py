"""
蓝图、全局路由实例化
"""

from admins import Index, LogoutView, LoginView
from flask import Blueprint
from flask_restful import Api
from users.api import *
from v2.api import *
from users.code import Code
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
docs.add_resource(UploadPart, '/file/upload/', endpoint="upload_part")
docs.add_resource(UploadMerge, '/file/merge/', endpoint="upload_success")
docs.add_resource(FileList, '/file/list/', endpoint="file_list")
docs.add_resource(FilePlayer, '/fileadmin/download/<filename>/', endpoint="video_player")
docs.add_resource(FileDownload, '/file/download/<filename>/', endpoint="file_download")
docs.add_resource(Login,'/user/login/', endpoint="user_login")
docs.add_resource(Register, '/user/register/', endpoint="user_reg")
docs.add_resource(Code, '/user/code/', endpoint="code")

docs.add_resource(GetPicByCate, '/img', endpoint="img")
docs.add_resource(GetUploadToken, '/token', endpoint='token')
docs.add_resource(UploadV2, '/upload/img', endpoint="upload_img")
docs.add_resource(EditCategory, '/put/cate', endpoint="put_cate")
