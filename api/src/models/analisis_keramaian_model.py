from src import db
from enum import Enum
from datetime import datetime

class StatusAnalisisKeramaian(Enum):
    SEPI = 'SEPI'
    NORMAL = 'NORMAL'
    PADAT = 'PADAT'

class AnalisisKeramaian(db.Model):
    __tablename__ = 'analisis_keramaian'

    id = db.Column(db.Integer, primary_key=True)
    id_keramaian = db.Column(db.Integer, db.ForeignKey('keramaian.id'), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(StatusAnalisisKeramaian), default=StatusAnalisisKeramaian.SEPI, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    keramaian = db.relationship('Keramaian', backref=db.backref('analisis_keramaian', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'id_keramaian': self.id_keramaian,
            'image': self.image,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'keramaian': self.keramaian.to_dict()
        }