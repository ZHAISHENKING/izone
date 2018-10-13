import jwt, datetime, time
from users.models import Users
from flask import jsonify, current_app
from . import common
import flask_login as login


class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                current_app.config["SECRET_KEY"],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def authenticate(self, username, password):
        """
        用户登录，登录成功返回token，将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        userInfo = Users.query.filter_by(username=username).first()
        if not userInfo:
            return common.falseReturn('用户不存在')
        else:
            if Users.check_password(Users, userInfo.password, password):
                login_time = int(time.time())
                # userInfo["login_time"] = login_time
                # userInfo.update()
                token = self.encode_auth_token(str(userInfo.id), login_time)
                print(token)
                login.login_user(userInfo)
                data = {
                    "jwt": token.decode(),
                    "username": userInfo.username,
                    "uid": userInfo.id
                }
                print(data)
                # data = common.user_authentication(data, userInfo)
                return common.trueReturn(data)
            else:
                return common.falseReturn('密码错误')

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # 10s过期测试
            # data = jwt.decode(auth_token, current_app.config["SECRET_KEY"], leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            data = jwt.decode(auth_token, current_app.config["SECRET_KEY"], options={'verify_exp': False})
            user = {}
            id = data["data"]["id"]
            user = Users.query.get(id=id)
            if user:
                userInfo = {
                    "id": user["id"],
                    "username": user["username"]
                }
                # userInfo = common.user_authentication(userInfo, user)
            else:
                raise jwt.InvalidTokenError

            return True, userInfo
        except jwt.ExpiredSignatureError:
            return False, 'Token过期'
        except jwt.InvalidTokenError:
            return False, '无效Token'
        except KeyError:
            return False, user
