from .models import Picture, Album, Video
from flask import render_template
from flask_restful import Resource
from utils.common import *
from admins import db
from flask import render_template as rt, make_response, Response, send_from_directory
from local_settings import *
from qiniu import Auth, put_data
# 需要填写你的 Access Key 和 Secret Key
access_key = QINIU_AK
secret_key = QINIU_SK
# 构建鉴权对象
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = QINIU_BUCKET
domain_prefix = QINIU_DOMAIN


class Upload(Resource):
    """上传图片"""
    def get(self):
        cate = Album.query.all()
        result = []
        for i in cate:
            result.append({"id": i.id, "title": i.title})
        return make_response(render_template("upload.html", category=result))

    @catch_exception
    def post(self):
        up = UpFile()
        data = request.values
        f = request.files["image"]
        filename = secure_filename(f.filename)
        mime = filename.rsplit(".")[1]
        with open(f, "rb") as file:
            qiniu_url = up.upload_img(file, mime)
            if qiniu_url:
                pic = Picture(
                    image_url=qiniu_url,
                    desc=data["desc"],
                    album=Album.query.filter_by(id=int(data["category"])).first()
                )
                db.session.add(pic)
                db.session.commit()
                return trueReturn(qiniu_url)
            else:
                return falseReturn("上传失败")


class GetAllImage(Resource):
    """获取图片"""
    @catch_exception
    def get(self):
        pic = Picture.query.all()
        result = []
        for i in pic:
            result.append({
                "id": i.id, "image_url": i.image_url,
                "desc": i.desc, "category": i.category.id
            })
        return trueReturn(result)


class GetAllCategory(Resource):
    """获取所有分类"""
    @catch_exception
    def get(self):
        cate = Album.query.all()
        result = []
        for i in cate:
            pic = Picture.query.filter_by(category=i).all()
            pic_list = []
            for j in pic:
                pic_list.append({"id": j.id,"image_url": j.image_url, "desc": j.desc})
            result.append({
                "id": i.id, "title": i.title, "desc": i.desc, "pic": pic_list
            })
        return trueReturn(result)


class GetPic(Resource):
    """根据分类id获取图片"""
    @catch_exception
    def post(self):
        id = request.values["id"]
        c = Album.query.filter_by(id=int(id)).first()
        pic = Picture.query.filter_by(category=c).all()
        result = []
        for i in pic:
            result.append({
                "id": i.id, "image_url": i.image_url,
                "desc": i.desc, "category": i.category.id
            })
        return trueReturn(result)


class VideoUpload(Resource):
    """上传视频"""
    def get(self):
        return make_response(rt('up.html'))

    @catch_exception
    def post(self):
        up = UpFile()
        data = request.values
        f = request.files["small_img"]
        filename = secure_filename(f.filename)
        f.save(filename)
        mime = filename.rsplit(".")[1]
        qiniu_url = up.upload_img(filename, mime)
        if not data["video"]:
            return falseReturn("上传失败")
        v = Video(
            video_url=data["video"],
            desc=data["desc"],
            small_img=qiniu_url,
            time_long=int(data["time_long"])

        )
        db.session.add(v)
        db.session.commit()
        return trueReturn(data["video"])


class GetAllVideo(Resource):
    """获取视频"""
    @catch_exception
    def get(self):
        v = Video.query.all()
        result = []
        for i in v:
            result.append({
                "id": i.id, "video_url": i.video_url,
                "desc": i.desc, "time_long": i.time_long,
                "small_img": i.small_img
            })
        return trueReturn(result)


class Home(Resource):
    def get(self):
        return make_response(rt('index.html'))


class UploadPart(Resource):
    def post(self):
        task = request.form.get('task_id')  # 获取文件的唯一标识符
        chunk = request.form.get('chunk', 0)  # 获取该分片在所有分片中的序号
        filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符

        upload_file = request.files['file']
        upload_file.save('/data/upload/%s' % filename)  # 保存分片到本地
        return make_response(rt('./up.html'))


class UploadMerge(Resource):
    def get(self):
        target_filename = request.args.get('filename')  # 获取上传文件的文件名
        task = request.args.get('task_id')  # 获取文件的唯一标识符
        chunk = 0  # 分片序号
        with open('/data/upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
            while True:
                try:
                    filename = '/data/upload/%s%d' % (task, chunk)
                    source_file = open(filename, 'rb')  # 按序打开每个分片
                    target_file.write(source_file.read())  # 读取分片内容写入新文件
                    source_file.close()
                except IOError as msg:
                    break

                chunk += 1
                os.remove(filename)  # 删除该分片，节约空间

        return make_response(rt('./up.html'))


class FileList(Resource):
    def get(self):
        files = os.listdir('/data/upload/')  # 获取文件目录
        files = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), files)  # 注意编码
        return make_response(rt('./list.html', files=files))


class FilePlayer(Resource):
    def get(self, filename):
        return send_from_directory("/data/upload", filename)


class FileDownload(Resource):
    def get(self, filename):
        # 流式读取
        def send_chunk():
            store_path = '/data/upload/%s' % filename
            with open(store_path, 'rb') as target_file:
                while True:
                    chunk = target_file.read(20 * 1024 * 1024)
                    if not chunk:
                        break
                    yield chunk
        return Response(send_chunk(), content_type='application/octet-stream')


def qiniu_upload_file(source_file, save_file_name):
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, save_file_name)
    ret, info = put_data(token, save_file_name, source_file.stream)
    if info.status_code == 200:
        return domain_prefix + save_file_name
    return None