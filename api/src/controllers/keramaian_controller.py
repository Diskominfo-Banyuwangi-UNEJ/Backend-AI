from flask import Blueprint, request, jsonify
from src.models.keramaian_model import Keramaian
from src.models.analisis_keramaian_model import AnalisisKeramaian, StatusAnalisisKeramaian
from src import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from functools import wraps

keramaian = Blueprint("keramaian", __name__)
analisis_keramaian = Blueprint("analisis_keramaian", __name__)

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except IntegrityError:
            db.session.rollback()
            return jsonify({
                'status': "error",
                'message': "Database integrity error occurred"
            }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': "error",
                'message': str(e)
            }), 500
    return decorated_function