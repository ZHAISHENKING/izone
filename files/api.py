from flask_restful import Resource
from utils.common import *
from .models import Video
from admins import db
from flask import render_template as rt, make_response, Response


class VideoUpload(Resource):
    """上传视频"""
    def get(self):
        return make_response(rt('up.html'))

    @catch_exception
    def post(self):
        data = request.values
        print(data["video"])
        if data["video"]:
            v = Video(
                video_url=data["video"],
                desc=data["desc"],
                small_img=data["small_img"],
                time_long=int(data["time_long"])

            )
            db.session.add(v)
            db.session.commit()
            return trueReturn(data["video"])
        else:
            return falseReturn("上传失败")


class GetAllVideo(Resource):
    """获取视频"""
    @catch_exception
    def get(self):
        v = Video.query.all()
        result = []
        if v:
            for i in v:
                obj = {
                    "id": i.id,
                    "video_url": i.video_url,
                    "desc": i.desc,
                    "time_long": i.time_long,
                    "small_img": i.small_img
                }
                result.append(obj)
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


class FileDwonload(Resource):
    def get(self, filename):
        def send_chunk():  # 流式读取
            store_path = '/data/upload/%s' % filename
            with open(store_path, 'rb') as target_file:
                while True:
                    chunk = target_file.read(20 * 1024 * 1024)
                    if not chunk:
                        break
                    yield chunk
        return Response(send_chunk(), content_type='application/octet-stream')