from admins import db
from users.models import Users


class Gatekeeper(db.Model):
    """权限"""
    __tablename__ = "gatekeeper"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(50))
    staff_required = db.Column(db.Boolean, default=False)
    percent = db.Column(db.Integer, default=0)
    white_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    whitelist = db.relationship('Users', backref=db.backref('gatekeeper'), lazy=True)

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

