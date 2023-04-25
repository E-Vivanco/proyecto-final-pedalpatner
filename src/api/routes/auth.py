import datetime
from api.models import User, Rol, Taller
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

bpAuth = Blueprint('bpAuth', __name__)

@bpAuth.route('/login', methods=['POST'])
def login_z():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email:
        return jsonify({"status": 422, "message": "Email is required"}), 422
    if not password:
        return jsonify({"status": 422, "message": "Password is required"}), 422

    user = User.query.filter_by(email=email).first()

    token_expires = datetime.timedelta(hours=2)
    access_token = create_access_token(identity=user.id, expires_delta= token_expires)

    data = {
    "access_token": access_token,
    "user": user.serialize_user(),
    "token_expires": token_expires.total_seconds()
    }

    return jsonify({ "status": 200, "message": "You have been logged", "data": data}), 200

# Logout debe ser hecho desde flux (front)