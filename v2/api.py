"""
新接口: izone-vue项目使用
"""
from v1.api import *


class GetPicByCate(Resource):
    """通过分类id获取图片"""
    def post(self):
        id = request.values["id"]
        c = Category.query.filter_by(id=int(id)).first()
        pic = Picture.query.filter_by(category=c).all()
        _list = []
        for i in pic:
            _list.append({
                "id": i.id, "image_url": i.image_url,
                "desc": i.desc, "category": i.category.id
            })
        result = {"id": id, "pic": _list, "desc": c.desc, "title": c.title}
        return trueReturn(result)


class GetUploadToken(Resource):
    """获取七牛token"""
    def post(self):
        token = q.upload_token(bucket_name)
        return trueReturn(token)