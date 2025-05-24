from src import db
from datetime import datetime
from enum import Enum

class StatusAnalisis(Enum):
    OK = 'OK'
    FULL = 'FULL'

class AnalisisTumpukan(db.Model):  # Must inherit from db.Model
    __tablename__ = 'analisis_tumpukan'
    
    id = db.Column(db.Integer, primary_key=True)
    id_tumpukan = db.Column(db.Integer, db.ForeignKey('tumpukan_sampah.id'), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(StatusAnalisis), default=StatusAnalisis.OK, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    tumpukan = db.relationship('TumpukanSampah', backref=db.backref('analisis_tumpukan', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'id_tumpukan': self.id_tumpukan,
            'image': self.image,
            'status': self.status.value if self.status else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tumpukan': self.tumpukan.to_dict()
        }