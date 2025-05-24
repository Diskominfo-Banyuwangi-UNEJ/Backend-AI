from flask import request, Blueprint, jsonify
from src.models.user_model import User, RoleEnum, NamaInstansi
from src import bcrypt, db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from functools import wraps

users = Blueprint("users", __name__)

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

def validate_user_data(data, required=True):
    errors = []
    required_fields = ['name_lengkap', 'email', 'username', 'password', 'role', 'nama_instansi']
    
    if required:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            errors.append(f"Missing required fields: {', '.join(missing_fields)}")
    
    if 'email' in data and not isinstance(data['email'], str):
        errors.append("Email must be a string")
    
    if 'username' in data and not isinstance(data['username'], str):
        errors.append("Username must be a string")
    
    if 'password' in data and not isinstance(data['password'], str):
        errors.append("Password must be a string")
    
    if 'role' in data and data['role'].upper() not in [role.name for role in RoleEnum]:
        errors.append(f"Invalid role. Must be one of: {', '.join([role.name for role in RoleEnum])}")
    
    if 'nama_instansi' in data and data['nama_instansi'].upper() not in [instansi.name for instansi in NamaInstansi]:
        errors.append(f"Invalid nama_instansi. Must be one of: {', '.join([instansi.name for instansi in NamaInstansi])}")
    
    return errors

@users.route('', methods=["POST"])
@handle_errors
def create_user():
    data = request.json
    errors = validate_user_data(data)
    
    if errors:
        return jsonify({
            'status': "failed",
            'message': "Validation failed",
            'errors': errors
        }), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'status': "failed",
            'message': "Email already exists"
        }), 409

    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'status': "failed",
            'message': "Username already exists"
        }), 409

    new_user = User(
        name_lengkap=data['name_lengkap'].strip(),
        email=data['email'].strip(),
        username=data['username'].strip(),
        password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
        role=RoleEnum[data['role'].upper()],
        nama_instansi=NamaInstansi[data['nama_instansi'].upper()]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'status': "success",
        'message': "User created successfully",
        'data': new_user.to_dict()
    }), 201

@users.route('', methods=["GET"])
@handle_errors
def get_all_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    role_filter = request.args.get('role', None)
    instansi_filter = request.args.get('instansi', None)
    
    query = User.query
    
    if role_filter:
        query = query.filter(User.role == RoleEnum[role_filter.upper()])
    
    if instansi_filter:
        query = query.filter(User.nama_instansi == NamaInstansi[instansi_filter.upper()])
    
    if 'search' in request.args:
        search = f"%{request.args['search']}%"
        query = query.filter(
            (User.name_lengkap.ilike(search)) |
            (User.email.ilike(search)) |
            (User.username.ilike(search))
        )
    
    if hasattr(User, sort_by):
        sort_column = getattr(User, sort_by)
        if order == 'desc':
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'status': "success",
        'message': "Users retrieved successfully",
        'data': [user.to_dict() for user in pagination.items],
        'pagination': {
            'total_items': pagination.total,
            'total_pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }
    }), 200

@users.route('/<int:id_user>', methods=["GET"])
@handle_errors
def get_user(id_user):
    user = User.query.get_or_404(
        id_user,
        description=f"User with id {id_user} not found"
    )
    
    return jsonify({
        'status': "success",
        'message': "User retrieved successfully",
        'data': user.to_dict()
    }), 200

@users.route('/<int:id_user>', methods=["PUT"])
@handle_errors
def update_user(id_user):
    data = request.json
    errors = validate_user_data(data, required=False)
    
    if errors:
        return jsonify({
            'status': "failed",
            'message': "Validation failed",
            'errors': errors
        }), 400

    user = User.query.get_or_404(
        id_user,
        description=f"User with id {id_user} not found"
    )

    if 'name_lengkap' in data:
        user.name_lengkap = data['name_lengkap'].strip()
    if 'email' in data:
        if User.query.filter(User.email == data['email'], User.id_user != id_user).first():
            return jsonify({
                'status': "failed",
                'message': "Email already exists"
            }), 409
        user.email = data['email'].strip()
    if 'username' in data:
        if User.query.filter(User.username == data['username'], User.id_user != id_user).first():
            return jsonify({
                'status': "failed",
                'message': "Username already exists"
            }), 409
        user.username = data['username'].strip()
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    if 'role' in data:
        user.role = RoleEnum[data['role'].upper()]
    if 'nama_instansi' in data:
        user.nama_instansi = NamaInstansi[data['nama_instansi'].upper()]

    user.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'status': "success",
        'message': "User updated successfully",
        'data': user.to_dict()
    }), 200

@users.route('/<int:id_user>', methods=["DELETE"])
@handle_errors
def delete_user(id_user):
    user = User.query.get_or_404(
        id_user,
        description=f"User with id {id_user} not found"
    )
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'status': "success",
        'message': "User deleted successfully"
    }), 200