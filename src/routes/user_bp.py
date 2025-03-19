from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController

user_bp = Blueprint('user', __name__)
controller = UserController()

@user_bp.route('', methods=['GET'])
def get_all():
    return jsonify(controller.get_all())

@user_bp.route('/<id>', methods=['GET'])
def get_by_id(id):
    return jsonify(controller.get_by_id(id))

@user_bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    return jsonify(controller.create(data))

@user_bp.route('/<id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    return jsonify(controller.update(id, data))

@user_bp.route('/<id>', methods=['DELETE'])
def delete(id):
    return jsonify(controller.delete(id))
