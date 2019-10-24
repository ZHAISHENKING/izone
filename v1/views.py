from admins import ModelView, db
from .models import *


class GatekeeperView(ModelView):
    column_searchable_list = (Gatekeeper.name, )
    column_labels = {
        "name": u"权限",
        "description": u"描述",
        "staff_required": u"管理员校验",
        "percent": u"百分比",
        "whitelist": u"白名单"
    }

    def __init__(self, **kwargs):
        super(GatekeeperView, self).__init__(Gatekeeper, db.session, **kwargs)


class VideoView(ModelView):
    column_labels = {
        "video_url": u"视频链接",
        "desc": u"描述",
        "time_long": u"时长",
        "small_img": u"封面图",
        "watch": u"观看次数"
    }

    def __init__(self, **kwargs):
        super(VideoView, self).__init__(Video, db.session, **kwargs)


class PicView(ModelView):
    column_labels = {
        "image_url": u"图片链接",
        "desc": u"描述",
        "category": u"分类"
    }

    def __init__(self, **kwargs):
        super(PicView, self).__init__(Picture, db.session, **kwargs)