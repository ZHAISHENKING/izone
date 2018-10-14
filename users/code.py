from flask import request, session, jsonify, current_app
from flask_restful import Resource
from utils.common import *
from admins import r
import gvcode


class Code(Resource):
    """
    图形验证码
    """
    @catch_exception
    def get(self):
        base64_str, code = gvcode.base64()

        # 把code存到session中
        r.set('verify_code', code)
        print(code)
        # 把base64_str 返回给用户
        return str(base64_str, "utf-8")


class VerifyCode(Resource):
    """
    验证code
    """
    @catch_exception
    def post(self):
        data = request.get_json()
        user_code = data['code'].lower()
        # 获取实际的验证码
        act_code = str(r.get('verify_code'), "utf8").lower()
        if user_code == act_code:
            return trueReturn("验证成功")
        else:
            return falseReturn("验证失败")


def verify(data):
    user_code = data['code'].lower()
    # 获取实际的验证码
    act_code = str(r.get('verify_code'), "utf8").lower()
    if user_code == act_code:
        return True
    else:
        return False
