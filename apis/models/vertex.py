from apis.models.model import db


class vertex(db.Model):
    __tablename__ = 'vertices'

    id = db.Column(db.BigInteger, primary_key=True)
    origin = db.Column(db.String(3))
    destiny = db.Column(db.String(3))
    cost = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('origin', 'destiny', name='_origin_destiny_uc'))

