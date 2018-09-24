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
