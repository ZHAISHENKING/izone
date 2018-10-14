from admins import ModelView, db
from .models import Gatekeeper


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