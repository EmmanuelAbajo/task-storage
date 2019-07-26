from app import db

class TokenBlacklist(db.Model):
    __tablename__ = 'tokenblacklist'
    id = db.Column(db.Integer,primary_key=True)
    jti = db.Column(db.String(128))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def isJtiBlacklisted(cls,jti):
        item = cls.query.filter_by(jti=jti).first()
        return bool(item)