import hashlib
import os, random, string
import qiniu
from flask import Flask, request
from werkzeug.utils import secure_filename
from datetime import datetime
from local_settings import *


# 请求成功
def trueReturn(data):
    return {
        "code": 0,
        "data": data,
        "msg": "请求成功"
    }


# 内部错误
def falseReturn(msg):
    return {
        "code": 1,
        "data": '',
        "msg": msg
    }


# 无权限
def VaildReturn(data):
    return {
        "code": 4,
        "data": data,
        "msg": "无效验证"
    }


# 数据库操作错误
def MongoReturn():
    return {
        "code": 2,
        "msg": "数据库操作错误"
    }


# 错误判断
def catch_exception(origin_func):
    def wrapper(self, *args, **kwargs):
        import sys
        import traceback
        from flask import current_app
        from sqlalchemy.exc import (
            SQLAlchemyError,
            NoSuchColumnError,
            NoSuchModuleError,
            NoForeignKeysError,
            NoReferencedColumnError,
            DisconnectionError
        )
        try:
            u = origin_func(self, *args, **kwargs)
            return u

        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            if request.json:
                param = dict(request.json)
            elif request.args:
                param = dict(request.args)
            else:
                param = ""
            result = "报错接口: %s\n报错方法: %s\n报错原因: %s\n报错参数: %s\n" % (
                request.path,
                origin_func.__name__,
                repr(e),
                param
            )
            for k, v in enumerate(traceback.extract_tb(exc_tb)):
                if k != 0:
                    result += "错误定位%d: %s\n" % (k, str(v))
            current_app.logger.error(result)
            return falseReturn(repr(e))

    return wrapper


# md5散列值
def md(t):
    hash1 = hashlib.md5()
    hash1.update(t.encode("UTF-8"))
    to_hash = hash1.hexdigest()
    return to_hash


class TimeFomat(object):
    """时间处理类"""

    def ms(self, d):
        import time
        # 给定时间元组,转换为秒
        return int(time.mktime(d.timetuple()))

    def dt(self, d):
        # 给定秒，转为datetime元组
        return datetime.fromtimestamp(d)


class UpFile(object):
    """
    上传
    """
    # 生成5位小写字母加数字的随机文件名
    @staticmethod
    def random_name():
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))

    # 上传至七牛云
    def upload_img(self, fn, sfx):
        key = self.random_name() + "." + sfx
        q = qiniu.Auth(QINIU_AK, QINIU_SK)
        token = q.upload_token(QINIU_BUCKET, key, 3600)
        ret, info = qiniu.put_data(token, key, fn)
        if (ret is not None) and ret['key'] == key and ret['hash'] == qiniu.etag(fn):
            return QINIU_DOMAIN + key
        else:
            self.notify("qiniu-fileup", "上传七牛云失败")
            return False

    @staticmethod
    # 调用系统通知
    def notify(title, text):
        os.system("osascript -e 'display notification \"{}\" with title \"{}\"'".format(text, title))


# JWT验证
def jwt_required(origin_func):
    def wrapper(self, *args, **kwargs):
        from flask import request
        from utils.auth import Auth

        # 请求头是否包含"jwt"
        if "jwt" in request.headers:
            is_vaild, info = Auth.decode_auth_token(request.headers['jwt'])
            if is_vaild:
                fn = origin_func(self, *args, **kwargs)
                return fn
            else:
                return falseReturn(info)
        else:
            return VaildReturn("")
    return wrapper


# 通过JWt获取用户信息
def get_user_info():
    from flask import request
    from utils.auth import Auth
    is_vaild, info = Auth.decode_auth_token(request.headers['jwt'])
    return info


# 判断超级用户
def super(origin_func):
    def wrapper(self, *args, **kwargs):
        from flask import request
        from utils.auth import Auth
        is_vaild, info = Auth.decode_auth_token(request.headers['jwt'])
        if info["is_super"]:
            fn = origin_func(self, *args, **kwargs)
            return fn
        else:
            return falseReturn("无权访问")
    return wrapper


# 返回前端用户权限
def user_authentication(data, user):
    from v1.models import Gatekeeper
    gates = Gatekeeper.query.all()

    for i in gates:
        data[i.name] = i.check_user(user)
    return data
