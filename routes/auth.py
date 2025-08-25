from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from models.user import User
from utils.database import db
from utils.neon_auth import NeonAuth

auth_bp = Blueprint('auth', __name__)

def get_request_json():
    """Safely get JSON data from request, handling missing Content-Type"""
    if not request.is_json:
        # Try to parse as JSON even if Content-Type is not set
        try:
            return request.get_json(force=True)
        except:
            return None
    return request.get_json()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = get_request_json()
        
        if not data:
            return jsonify({'error': 'Request must be JSON with Content-Type: application/json'}), 415
        
        # Check required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User already exists'}), 400
        
        # Create user using Neon Auth or local authentication
        user = NeonAuth.create_user(
            email=data['email'],
            password=data['password'],
            user_data={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone': data.get('phone'),
                'address': data.get('address')
            }
        )
        
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = get_request_json()
        
        if not data:
            return jsonify({'error': 'Request must be JSON with Content-Type: application/json'}), 415
        
        # Check required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate user using Neon Auth or local authentication
        user = NeonAuth.authenticate_user(data['email'], data['password'])
        
        if user:
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        data = get_request_json()
        
        if not data:
            return jsonify({'error': 'Request must be JSON with Content-Type: application/json'}), 415
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'address' in data:
            user.address = data['address']
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully', 'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = get_request_json()
        
        if not data:
            return jsonify({'error': 'Request must be JSON with Content-Type: application/json'}), 415
        
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user:
            # Return success even if user doesn't exist to prevent email enumeration
            return jsonify({'message': 'If the email exists, a password reset link has been sent'}), 200
        
        # Send password reset using Neon Auth or alternative method
        success = NeonAuth.send_password_reset(email)
        
        if success:
            return jsonify({'message': 'If the email exists, a password reset link has been sent'}), 200
        else:
            return jsonify({'error': 'Failed to process password reset'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = get_request_json()
        
        if not data:
            return jsonify({'error': 'Request must be JSON with Content-Type: application/json'}), 415
        
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not token or not new_password:
            return jsonify({'error': 'Token and new password are required'}), 400
        
        # Verify token
        payload = NeonAuth.verify_password_reset_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 400
        
        user_id = payload.get('sub')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Password reset successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400