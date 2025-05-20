from src import db
from enum import Enum
from datetime import datetime

class StatusPengerjaan(Enum):
    BARU    = 'BARU'
    DIBACA  = 'DIBACA'
    SELESAI = 'SELESAI'

class Kategori(Enum):
    KERAMAIAN       = 'KERAMAIAN'
    TUMPUKAN_SAMPAH = 'TUMPUKAN_SAMPAH'

class Laporan(db.Model):
    __tablename__   = 'laporan'

    id                  = db.Column(db.Integer, primary_key=True)
    judul_laporan       = db.Column(db.Text, nullable=False)
    deskripsi           = db.Column(db.Text, nullable=False)
    estimasi            = db.Column(db.String(20), nullable=False)
    kategori            = db.Column(db.Enum(Kategori))
    status_pengerjaan   = db.Column(db.Enum(StatusPengerjaan))
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at          = db.Column(db.DateTime, onupdate=datetime.utcnow)
    id_user             = db.Column(db.Integer, db.ForeignKey('User.id_user'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'judul_laporan': self.judul_laporan,
            'deskripsi': self.deskripsi,
            'estimasi': self.estimasi,
            'kategori': self.kategori.value if self.kategori else None,  # Serialize enum value
            'status_pengerjaan': self.status_pengerjaan.value if self.status_pengerjaan else None,  # Serialize enum value
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'id_user': self.id_user
        }