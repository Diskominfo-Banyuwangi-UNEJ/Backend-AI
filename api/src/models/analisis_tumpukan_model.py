from src import db
from datetime import datetime

class AnalisisTumpukan:
    __tablename__ = 'analisis_tumpukan'

    id = db.Column(db.Integer, primary_key=True)
    id_tumpukan = db.Column(db.Integer, foreignKey='tumpukan_sampah.id', nullable=False)
    image = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('OK', 'BAD'), default='OK', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    tumpukan = db.relationship('TumpukanSampah', backref='analisis_tumpukan')

    def to_dict(self):
        return {
            'id': self.id,
            'id_tumpukan': self.id_tumpukan,
            'image': self.image,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }