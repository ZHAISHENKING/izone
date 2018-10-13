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
        except AttributeError as e:
            current_app.logger.error(e)
            return "参数错误"
        except (
                SQLAlchemyError,
                NoSuchColumnError,
                NoSuchModuleError,
                NoForeignKeysError,
                NoReferencedColumnError,
                DisconnectionError
        ) as e:
            current_app.logger.error(e)
            return MongoReturn()
        except TypeError as e:
            current_app.logger.error(e)
            return falseReturn("TypeError")
        except Exception as e:
            current_app.logger.error(e)
            return falseReturn("Error")

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
        ret, info = qiniu.put_file(token, key, fn)
        if (ret is not None) and ret['key'] == key and ret['hash'] == qiniu.etag(fn):
            return QINIU_DOMAIN + key
        else:
            self.notify("qiniu-fileup", "上传七牛云失败")
            return False

    @staticmethod
    # 调用系统通知
    def notify(title, text):
        os.system("osascript -e 'display notification \"{}\" with title \"{}\"'".format(text, title))
