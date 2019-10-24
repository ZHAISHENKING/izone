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
    # 分类外键
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship("Category", backref=db.backref('picture'))

    def __repr__(self):
        return "<Picture %r>" % self.id


class Category(db.Model):
    """分类"""
    __tablename__ = "category"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(30))
    desc = db.Column(db.String(250))

    def __repr__(self):
        return "<Category %r>" % self.title
