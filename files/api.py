from flask_restful import Resource
from utils.common import *
from .models import Video
from admins import db
from flask import render_template, make_response


class VideoUpload(Resource):
    """上传视频"""
    def get(self):
        return make_response(render_template('video.html'))

    @catch_exception
    def post(self):
        up = UpFile()
        data = request.values
        f = request.files["video"]
        filename = secure_filename(f.filename)
        f.save(filename)
        mime = filename.rsplit(".")[1]
        qiniu_url = up.upload_img(filename, mime)
        if qiniu_url:
            v = Video(
                video_url=qiniu_url,
                desc=data["desc"],
                small_img=data["small_img"],
                time_long=int(data["time_long"])

            )
            db.session.add(v)
            db.session.commit()
            return trueReturn(qiniu_url)
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
        return make_response(render_template('index.html'))
