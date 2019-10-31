from sqlalchemy.exc import SQLAlchemyError
from admins import db
from datetime import datetime


class Picture(db.Model):
    """
    图片
    """
    __tablename__ = "picture"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    image_url = db.Column(db.String(100))
    desc = db.Column(db.String(80))
    create_at = db.Column(db.Date, default=datetime.now)
    # 相册外键
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album', backref=db.backref('picture'))

    def __repr__(self):
        return "<Picture %r>" % self.id


class Video(db.Model):
    """
    视频
    """
    __tablename__ = "video"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    video_url = db.Column(db.String(100))
    desc = db.Column(db.String(80))
    time_long = db.Column(db.Integer)
    small_img = db.Column(db.String(100))
    watch = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<Video %r>" % self.id


class Album(db.Model):
    """相册"""
    __tablename__ = "album"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(30))
    desc = db.Column(db.String(250))
    cate = db.Column(db.Enum(
        '最爱', '风景', '人物', '动物', '游记', '卡通', '生活', '其他'
    ), server_default='最爱', nullable=False)
    cover = db.Column(db.String(250))
    create_at = db.Column(db.Date, default=datetime.now)

    def __repr__(self):
        return "<Album %r>" % self.title


class Gatekeeper(db.Model):
    """权限"""
    __tablename__ = "gatekeeper"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(50))
    staff_required = db.Column(db.Boolean, default=False)
    percent = db.Column(db.Integer, default=0)
    whitelist = db.relationship('Users', backref='user', lazy=True)

    def check_user(self, user):
        """ Staff user can pass check anywhere.
            Anonymous user can not pass check
            if staff required then white list is disabled.
            else check whitelist
            then check the percent
            """
        if not user:
            return False

        if self.staff_required:
            return False

        if user in self.whitelist:
            return True
        else:
            return False

        # hash = hashlib.md5(str(user.id).encode('utf-8'))[-4:]
        # return int(hash, 16) % 100 < self.percent

    def __repr__(self):
        return '%s' % self.name


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason