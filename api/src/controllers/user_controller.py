from flask import request, Blueprint, jsonify
from src.models.user_model import User, GenderEnum, RoleEnum
from src import bcrypt, db
from datetime import datetime

users = Blueprint("users", __name__)

@users.route('', methods=["POST"])
def create_user():
    try:
        data = request.json
        required_fields = ['name_lengkap', 'email', 'username', 'password', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({'status': "failed", "message": "Missing required fields"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'status': "failed", "message": "Email already exists"}), 409

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'status': "failed", "message": "Username already exists"}), 409

        new_user = User(
            name_lengkap=data['name_lengkap'],
            email=data['email'],
            username=data['username'],
            password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            role=RoleEnum[data['role'].upper()],
            jenis_kelamin=GenderEnum[data.get('jenis_kelamin', 'OTHER').upper()],
            no_telepon=data.get('no_telepon'),
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'status': "success",
            "message": "User created successfully",
            "data": new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': "error", "message": str(e)}), 500


@users.route('', methods=["GET"])
def get_all_users():
    try:
        users = User.query.all()
        return jsonify({
            'status': "success",
            'message': "Users retrieved successfully",
            'data': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'status': "error", "message": str(e)}), 500


@users.route('/<int:user_id>', methods=["GET"])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': "failed", "message": "User not found"}), 404

        return jsonify({
            'status': "success",
            "data": user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'status': "error", "message": str(e)}), 500


@users.route('/<int:user_id>', methods=["PUT"])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': "failed", "message": "User not found"}), 404

        data = request.json

        if 'name_lengkap' in data:
            user.name_lengkap = data['name_lengkap']
        if 'email' in data:
            user.email = data['email']
        if 'username' in data:
            user.username = data['username']
        if 'password' in data:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        if 'role' in data:
            user.role = RoleEnum[data['role'].upper()]
        if 'jenis_kelamin' in data:
            user.jenis_kelamin = GenderEnum[data['jenis_kelamin'].upper()]
        if 'no_telepon' in data:
            user.no_telepon = data['no_telepon']

        db.session.commit()

        return jsonify({
            'status': "success",
            "message": "User updated successfully",
            "data": user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': "error", "message": str(e)}), 500