from flask import request, session, current_app
from flask_restful import Resource
from .models import *
from .code import verify
from util.common import *
from util.auth import Auth
from .form import LoginForm, RegistrationForm, login


class Register(Resource):
    """用户注册"""
    def __init__(self):
        self.form = RegistrationForm(request.form)

    @catch_exception
    def post(self):
        data = request.values

        if data["username"]:
            if Users.query.filter_by(username=data["username"]).first():
                return falseReturn("用户已存在")
            else:
                if verify(data):
                    user = Users(
                        username=data["username"],
                        password=Users.set_password(Users, data["password"])
                    )
                    db.session.add(user)
                    db.session.commit()
                    if user.id:
                        return Auth.authenticate(Auth, data["username"], data["password"])
                    else:
                        return falseReturn("注册失败")
                else:
                    return falseReturn("验证码错误")
        else:
            return falseReturn("请输入用户名")


class Login(Resource):
    """用户登录"""
    def __init__(self):
        self.form = LoginForm(request.form)

    @catch_exception
    def post(self):
        data = request.values
        username = data["username"]
        password = data["password"]
        if not username or not password:
            return falseReturn("用户名和密码不能为空")
        else:
            return Auth.authenticate(Auth, username, password)


# class ResetPassword(Resource):
#     """修改密码"""
#     @jwt_required
#     @catch_exception
#     def post(self):
#         data = request.get_json()
#         try:
#             phone = data["phone"]
#             password = data["password"]
#             reset = data["reset"]
#         except Exception as e:
#             return falseReturn("参数错误")
#         user = User.objects.get(phone=phone)
#         if User.check(user.password, password):
#             user.update(password=User.set(reset))
#             return trueReturn("修改成功")
#         else:
#             return falseReturn("原密码错误")
#
#
# class ForgetPass(Resource):
#     """忘记密码"""
#     @catch_exception
#     def post(self):
#         data = request.json
#         phone = data["phone"]
#         reset = data["reset"]
#
#         if r.get("slag") == b'1':
#             user = User.objects.get(phone=phone)
#             user.update(password=User.set(reset))
#             r.set("slag", "0")
#             return trueReturn("修改成功")
#         else:
#             return falseReturn("手机验证失败")

