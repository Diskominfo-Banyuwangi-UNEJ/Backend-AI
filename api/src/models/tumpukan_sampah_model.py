from src import db
from datetime import datetime

class TumpukanSampah(db.Model):
    __tablename__ = 'tumpukan_sampah'

    id = db.Column(db.Integer, primary_key=True)
    nama_lokasi = db.Column(db.String(35), nullable=False)
    alamat = db.Column(db.String(35), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nama_lokasi': self.nama_lokasi,
            'alamat': self.alamat,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }