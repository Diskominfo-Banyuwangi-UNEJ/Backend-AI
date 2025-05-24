from src import db
from enum import Enum
from datetime import datetime

class RoleEnum(Enum):
    ADMIN = 1
    PEMERINTAH = 2

class NamaInstansi(Enum):
    KOMINFO = "Kementerian Komunikasi dan Informatika"
    DISHUB = "Dinas Perhubungan"
    DLH = "Dinas Lingkungan Hidup"
    SATPOL_PP = "Satuan Polisi Pamong Praja"

class User(db.Model):
    __tablename__ = 'User'
    
    id_user = db.Column(db.Integer(), primary_key=True, nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    nama_instansi = db.Column(db.Enum(NamaInstansi), nullable=False)
    name_lengkap = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(35), nullable=False, unique=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'role': self.role.name if self.role else None,
            'nama_instansi': self.nama_instansi.value if self.nama_instansi else None,
            'name_lengkap': self.name_lengkap,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

