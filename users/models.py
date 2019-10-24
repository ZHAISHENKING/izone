from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from admins import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    cover = db.Column(db.String(250))
    username = db.Column(db.String(250),  unique=True, nullable=False)
    password = db.Column(db.String(250))
    gate = db.Column(db.Integer, db.ForeignKey('gatekeeper.id'))
    login_time = db.Column(db.Integer)
    begin_at = db.Column(db.Date, default=datetime.now)
    end_at = db.Column(db.Date, default=datetime.now)

    def __repr__(self):
        return self.username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def get(self, id):
        return self.query.filter_by(id=id).first()

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason