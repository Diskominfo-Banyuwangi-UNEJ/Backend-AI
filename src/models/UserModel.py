from datetime import datetime
from config import db

class User(db.Model):
    __tablename__   = "users"
    id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_lengkap    = db.Column(db.String(30), nullable=False)
    tanggal_lahir   = db.Column(db.DateTime, nullable=False)
    email   = db.Column(db.String(35), nullable=False)
    no_telepon  = db.Column(db.String(13), nullable=False)
    jenis_kelaim = db.Column(db.Enum("Laki-laki", "Perempuan"), nullable=False)
    username    = db.Column(db.String(15), nullable=False)
    password    = db.Column(db.String(25), nullable=False)