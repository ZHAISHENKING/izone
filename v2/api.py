"""
新接口: izone-vue项目使用
"""
from v1.api import *


class GetPicByCate(Resource):
    """通过分类id获取图片"""
    def post(self):
        id = request.values["id"]
        c = Album.query.filter_by(id=int(id)).first()
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


class UploadV2(Resource):
    """
    上传图片
    @:param id: category id
    @:param file: image
    """
    @catch_exception
    def post(self):
        up = UpFile()
        data = request.values
        f = request.files["file"]
        filename = secure_filename(f.filename)
        try:
            mime = filename.rsplit(".")[1]
        except Exception:
            mime = None
        qiniu_url = up.upload_img(f.read(), mime)
        if qiniu_url:
            pic = Picture(
                image_url=qiniu_url,
                album=Album.query.filter_by(id=int(data["id"])).first()
            )
            db.session.add(pic)
            db.session.commit()
            return trueReturn(qiniu_url)
        else:
            return falseReturn("上传失败")


class EditCategory(Resource):
    """
    编辑分类
    @:param: id: category id
    @:param: title: new category name
    """
    @catch_exception
    def post(self):
        data = request.values
        category = Album.query.filter_by(id=int(data["id"])).first()
        if not category:
            return falseReturn("分类不存在")
        category.title = data["title"]
        db.session.add(category)
        db.session.commit()
        return trueReturn("编辑成功")


class DeleteImg(Resource):
    """
    删除图片
    @:param: ids: picture id array
    """
    @catch_exception
    def post(self):
        data = request.values
        ids = data["ids"].split(',')
        ids = [int(i) for i in ids]
        Picture.query.filter(Picture.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return trueReturn("删除成功")


class CreateAlbum(Resource):
    """
    创建相册
    @:param: title: 相册名
    @:param: desc: 相册描述
    """
    @catch_exception
    def post(self):
        data = request.values
        cate = Album(
            title=data['title'],
            desc=data["desc"]
        )
        db.session.add(cate)
        db.session.commit()
        return trueReturn(cate.id)