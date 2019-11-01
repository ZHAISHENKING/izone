"""
新接口: izone-vue项目使用
"""
from v1.api import *

cate_choice = dict({
    (0, '最爱'),
    (1, "风景"),
    (2, "人物"),
    (3, "动物"),
    (4, "游记"),
    (5, "卡通"),
    (6, "生活"),
    (7, "其他")
})


class GetPicByCate(Resource):
    """通过分类id获取图片"""
    def post(self):
        id = request.values["id"]
        c = Album.query.filter_by(id=int(id)).first()
        pic = Picture.query.filter_by(album=c).all()
        _list = []
        for i in pic:
            _list.append({
                "id": i.id, "image_url": i.image_url,
                "desc": i.desc, "album": i.album.id,
                "create_at": str(i.create_at)
            })
        result = {"id": id, "pic": _list,
                  "desc": c.desc, "title": c.title,
                  'cover': c.cover, 'cate': c.cate}
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
    编辑相册
    @:param: id: category id
    @:param: title: new category name
    """
    @catch_exception
    def post(self):
        data = request.values
        category = Album.query.filter_by(id=int(data["id"])).first()
        if not category:
            return falseReturn("分类不存在")
        if 'title' in data:
            category.title = data.get('title')
        if 'desc' in data:
            category.desc = data.get("desc")
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
        album = Album(
            title=data['title'],
            desc=data["desc"],
            cate=data["cate"]
        )
        db.session.add(album)
        db.session.commit()
        return trueReturn(album.id)


class AuthToken(Resource):
    """
    鉴权接口
    @:param: token
    """
    @catch_exception
    def post(self):
        from utils.auth import Auth
        data = request.values
        token = data.get("token")
        auth, info = Auth().decode_auth_token(token)
        if auth:
            return trueReturn(info)
        else:
            return falseReturn(info)


class UploadCover(Resource):
    """
    上传头像
    @:param: file
    """
    @catch_exception
    @jwt_required
    def post(self):
        up = UpFile()
        f = request.files["file"]
        filename = secure_filename(f.filename)
        try:
            mime = filename.rsplit(".")[1]
        except Exception:
            mime = None
        qiniu_url = up.upload_img(f.read(), mime)
        user = get_user()
        if qiniu_url:
            user.cover = qiniu_url
            db.session.add(user)
            db.session.commit()
            return trueReturn(qiniu_url)
        else:
            return falseReturn("上传失败")


class SocketAPI(Resource):
    @catch_exception
    def get(self):
        return make_response(render_template('index.html'))
