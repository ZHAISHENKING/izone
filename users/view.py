from .models import *
from admins import ModelView


class MyUserlView(ModelView):
    column_list = (
        'id', 'username', "cover", 'login_time'
    )
    column_labels = {
        "id": u"序号",
        "username": u"姓名",
        "login_time": u"上次登录"
    }
    # column_searchable_list = (
    #     Users.username
    # )

    def __init__(self, **kwargs):
        super(MyUserlView, self).__init__(Users, db.session, **kwargs)
