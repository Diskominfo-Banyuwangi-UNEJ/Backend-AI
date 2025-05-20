from flask import request, Blueprint, jsonify
from src.models.tumpukan_sampah_model import TumpukanSampah
from src.models.analisis_tumpukan_model import AnalisisTumpukan, StatusAnalisis
from src import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from functools import wraps

tumpukan_sampah = Blueprint("tumpukan_sampah", __name__)
analisis_tumpukan = Blueprint("analisis_tumpukan", __name__)

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

def validate_tumpukan_sampah_data(data, required=True):
    errors = []
    required_fields = ['nama_lokasi', 'alamat', 'latitude', 'longitude']
    
    if required:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            errors.append(f"Missing required fields: {', '.join(missing_fields)}")
    
    if 'latitude' in data:
        try:
            lat = float(data['latitude'])
            if not -90 <= lat <= 90:
                errors.append("Latitude must be between -90 and 90")
        except ValueError:
            errors.append("Latitude must be a number")
    
    if 'longitude' in data:
        try:
            lon = float(data['longitude'])
            if not -180 <= lon <= 180:
                errors.append("Longitude must be between -180 and 180")
        except ValueError:
            errors.append("Longitude must be a number")
    
    return errors

@analisis_tumpukan.route('/getAll', methods=["GET"])
@handle_errors
def get_all_analisis_tumpukan():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    status_filter = request.args.get('status', None)

    query = AnalisisTumpukan.query

    if status_filter:
        query = query.filter(AnalisisTumpukan.status == StatusAnalisis(status_filter))

    if 'search' in request.args:
        search = f"%{request.args['search']}%"
        query = query.join(AnalisisTumpukan.tumpukan).filter(
            (TumpukanSampah.nama_lokasi.ilike(search)) |
            (TumpukanSampah.alamat.ilike(search))
        )

    if hasattr(AnalisisTumpukan, sort_by):
        sort_column = getattr(AnalisisTumpukan, sort_by)
        if order == 'desc':
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'status': "success",
        'message': "Analisis Tumpukan retrieved successfully",
        'data': [item.to_dict() for item in pagination.items],
        'pagination': {
            'total_items': pagination.total,
            'total_pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }
    }), 200

@tumpukan_sampah.route('', methods=["POST"])
@handle_errors
def create_tumpukan_sampah():
    data = request.json
    errors = validate_tumpukan_sampah_data(data)
    
    if errors:
        return jsonify({
            'status': "failed",
            'message': "Validation failed",
            'errors': errors
        }), 400

    new_tumpukan_sampah = TumpukanSampah(
        nama_lokasi=data['nama_lokasi'].strip(),
        alamat=data['alamat'].strip(),
        latitude=float(data['latitude']),
        longitude=float(data['longitude'])
    )

    db.session.add(new_tumpukan_sampah)
    db.session.commit()

    return jsonify({
        'status': "success",
        'message': "Tumpukan Sampah created successfully",
        'data': new_tumpukan_sampah.to_dict()
    }), 201

@tumpukan_sampah.route('', methods=["GET"])
@handle_errors
def get_all_tumpukan_sampah():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    
    query = TumpukanSampah.query
    
    if 'search' in request.args:
        search = f"%{request.args['search']}%"
        query = query.filter(
            (TumpukanSampah.nama_lokasi.ilike(search)) |
            (TumpukanSampah.alamat.ilike(search))
        )
    
    # Sorting
    if hasattr(TumpukanSampah, sort_by):
        sort_column = getattr(TumpukanSampah, sort_by)
        if order == 'desc':
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'status': "success",
        'message': "Tumpukan Sampah retrieved successfully",
        'data': [item.to_dict() for item in pagination.items],
        'pagination': {
            'total_items': pagination.total,
            'total_pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }
    }), 200

@tumpukan_sampah.route('/<int:tumpukan_sampah_id>', methods=["GET"])
@handle_errors
def get_tumpukan_sampah(tumpukan_sampah_id):
    tumpukan_sampah = TumpukanSampah.query.get_or_404(
        tumpukan_sampah_id,
        description=f"Tumpukan Sampah with id {tumpukan_sampah_id} not found"
    )
    
    return jsonify({
        'status': "success",
        'message': "Tumpukan Sampah retrieved successfully",
        'data': tumpukan_sampah.to_dict()
    }), 200

@tumpukan_sampah.route('/<int:tumpukan_sampah_id>', methods=["PUT"])
@handle_errors
def update_tumpukan_sampah(tumpukan_sampah_id):
    data = request.json
    errors = validate_tumpukan_sampah_data(data, required=False)
    
    if errors:
        return jsonify({
            'status': "failed",
            'message': "Validation failed",
            'errors': errors
        }), 400

    tumpukan_sampah = TumpukanSampah.query.get_or_404(
        tumpukan_sampah_id,
        description=f"Tumpukan Sampah with id {tumpukan_sampah_id} not found"
    )

    if 'nama_lokasi' in data:
        tumpukan_sampah.nama_lokasi = data['nama_lokasi'].strip()
    if 'alamat' in data:
        tumpukan_sampah.alamat = data['alamat'].strip()
    if 'latitude' in data:
        tumpukan_sampah.latitude = float(data['latitude'])
    if 'longitude' in data:
        tumpukan_sampah.longitude = float(data['longitude'])

    db.session.commit()

    return jsonify({
        'status': "success",
        'message': "Tumpukan Sampah updated successfully",
        'data': tumpukan_sampah.to_dict()
    }), 200

@tumpukan_sampah.route('/<int:tumpukan_sampah_id>', methods=["DELETE"])
@handle_errors
def delete_tumpukan_sampah(tumpukan_sampah_id):
    tumpukan_sampah = TumpukanSampah.query.get_or_404(
        tumpukan_sampah_id,
        description=f"Tumpukan Sampah with id {tumpukan_sampah_id} not found"
    )
    
    db.session.delete(tumpukan_sampah)
    db.session.commit()
    
    return jsonify({
        'status': "success",
        'message': "Tumpukan Sampah deleted successfully"
    }), 200