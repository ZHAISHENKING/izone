from admins import db


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


class Staff(db.Model):
    """测试model,可用此model创建数据来测试sqlchemy的聚合、查询等方法"""
    __tablename__ = "staff"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100))
    score = db.Column(db.Integer, default=True)
    depart = db.ARRAY(db.String(100))

    def __repr__(self):
        return "<Staff %r>" % self.id