from .models import *
from admins import ModelView


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