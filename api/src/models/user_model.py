from src import db
from enum import Enum
from datetime import datetime

class GenderEnum(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class RoleEnum(Enum):
    ADMIN = 1
    USER = 2
    STAFF = 3

class User(db.Model):
    __tablename__ = 'User'
    
    id_user = db.Column(db.Integer(), primary_key=True, nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    name_lengkap = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(35), nullable=False, unique=True)
    no_telepon = db.Column(db.String(13), nullable=False)
    jenis_kelamin = db.Column(db.Enum(GenderEnum), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'role': self.role.name if self.role else None,
            'name_lengkap': self.name_lengkap,
            'email': self.email,
            'no_telepon': self.no_telepon,
            'jenis_kelamin': self.jenis_kelamin.name if self.jenis_kelamin else None,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

