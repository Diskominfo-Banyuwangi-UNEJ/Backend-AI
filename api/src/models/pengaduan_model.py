from src import db
from datetime import datetime
from enum import Enum

class KaterogiPengaduan(Enum):
    KERAMAIAN       = 'KERAMAIAN'
    TUMPUKAN_SAMPAH = 'TUMPUKAN_SAMPAH'

class StatusPengaduan(Enum):
    BARU    = 'BARU'
    DIBACA  = 'DIBACA'
    SELESAI = 'SELESAI'

class Pengaduan(db.Model):
    __tablename__ = 'pengaduan'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('User.id_user'), nullable=False)
    katerogi_pengaduan = db.Column(db.Enum(KaterogiPengaduan), nullable=False)
    status_pengaduan = db.Column(db.Enum(StatusPengaduan), default=StatusPengaduan.BARU, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('pengaduan', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'id_user': self.id_user,
            'katerogi_pengaduan': self.katerogi_pengaduan.value if self.katerogi_pengaduan else None,
            'status_pengaduan': self.status_pengaduan.value if self.status_pengaduan else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }