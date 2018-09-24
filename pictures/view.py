from .models import *
from admins import ModelView


class PicView(ModelView):
    column_labels = {
        "image_url": u"图片链接",
        "desc": u"描述",
        "category": u"分类"
    }

    def __init__(self, **kwargs):
        super(PicView, self).__init__(Picture, db.session, **kwargs)