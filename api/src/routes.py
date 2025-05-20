from flask import Blueprint
from src.controllers.user_controller import users
from src.controllers.auth_controller import auth
from src.controllers.tumpukan_sampah_controller import tumpukan_sampah, analisis_tumpukan
from src.controllers.laporan_controller import laporan
from src.docs import docs_bp

api = Blueprint('api', __name__)

api.register_blueprint(users, url_prefix='/users')
api.register_blueprint(auth, url_prefix='/auth')
api.register_blueprint(tumpukan_sampah, url_prefix='/tumpukan_sampah')
api.register_blueprint(analisis_tumpukan, url_prefix='/analisis_tumpukan')
api.register_blueprint(laporan, url_prefix='/laporan')
api.register_blueprint(docs_bp) 