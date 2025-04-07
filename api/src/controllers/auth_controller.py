import os
import jwt
from flask import Blueprint, request, jsonify
from src.models.user_model import User
from src import bcrypt, db
from datetime import datetime, timedelta


auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        required_fields = ['email', 'password']
        if 'email' and 'password' in data:
            user = User.query.filter_by(email=data['email']).first()

            if user:
                if bcrypt.check_password_hash(user.password, data['password']):
                    payload = {
                        'iat': datetime.utcnow(),
                        'id_user': user.id_user,
                        'email': user.email,
                        'username': user.username,
                    }

                    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
                    response = jsonify({
                        'status': "success",
                        'message': "User logged in successfully",
                        'token': token
                    })

                    response.set_cookie(
                        key="token",
                        value=token,
                        httponly=True,
                        secure=True,
                        samesite="Lax",
                        expires=datetime.utcnow() + timedelta(days=1)
                    )

                    return response, 200
                else:
                    return jsonify({'status': "failed", "message": "User password doesn't match"}), 401
            else:
                return jsonify({'status': "failed", "message": "User Record dosen't exist"}), 404
        else:
            return jsonify({'status': "failed", "message": "Missing required fields"}), 400
    except Exception as e:
        return jsonify({'status': "error", "message": str(e)}), 500


@auth.route('/logout', methods=['POST'])
def logout():
    try:
        response = jsonify({
            'status': "success",
            'message': "Logged out successfully"
        })

        # Hapus cookie 'token'
        response.set_cookie(
            key='token',
            value='',
            expires=0,
            httponly=True
        )

        return response, 200

    except Exception as e:
        return jsonify({'status': "error", "message": str(e)}), 500