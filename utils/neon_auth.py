import requests
import jwt
from flask import current_app
from datetime import datetime, timedelta
from models.user import User
from utils.database import db

class NeonAuth:
    """Handles authentication using Neon's authentication system"""
    
    @staticmethod
    def create_user(email, password, user_data):
        """
        Create a new user using Neon Auth (if enabled) or fallback to local auth
        
        Args:
            email: User email
            password: User password
            user_data: Additional user data
        
        Returns:
            User: The created user object
        """
        # If Neon Auth is enabled, create user through Neon API
        if current_app.config.get('NEON_AUTH_ENABLED'):
            try:
                # This is a hypothetical implementation as Neon Auth API details may vary
                response = requests.post(
                    f"{current_app.config['NEON_AUTH_URL']}/users",
                    headers={
                        "Authorization": f"Bearer {current_app.config['NEON_API_KEY']}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "email": email,
                        "password": password,
                        "user_metadata": user_data
                    }
                )
                
                if response.status_code == 201:
                    neon_user_id = response.json().get('id')
                    # Create local user record with reference to Neon user ID
                    user = User(
                        email=email,
                        first_name=user_data.get('first_name'),
                        last_name=user_data.get('last_name'),
                        phone=user_data.get('phone'),
                        address=user_data.get('address'),
                        neon_user_id=neon_user_id
                    )
                    db.session.add(user)
                    db.session.commit()
                    return user
                else:
                    # Fallback to local authentication if Neon Auth fails
                    return NeonAuth._create_local_user(email, password, user_data)
                    
            except Exception as e:
                current_app.logger.error(f"Neon Auth error: {str(e)}")
                # Fallback to local authentication
                return NeonAuth._create_local_user(email, password, user_data)
        else:
            # Use local authentication
            return NeonAuth._create_local_user(email, password, user_data)
    
    @staticmethod
    def _create_local_user(email, password, user_data):
        """Create user with local authentication"""
        user = User(
            email=email,
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            phone=user_data.get('phone'),
            address=user_data.get('address')
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate a user using Neon Auth or local authentication
        
        Args:
            email: User email
            password: User password
        
        Returns:
            User: Authenticated user or None
        """
        # If Neon Auth is enabled, authenticate through Neon API
        if current_app.config.get('NEON_AUTH_ENABLED'):
            try:
                # This is a hypothetical implementation
                response = requests.post(
                    f"{current_app.config['NEON_AUTH_URL']}/token",
                    headers={
                        "Authorization": f"Bearer {current_app.config['NEON_API_KEY']}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "email": email,
                        "password": password
                    }
                )
                
                if response.status_code == 200:
                    # Find user by email
                    user = User.query.filter_by(email=email).first()
                    return user
                else:
                    # Fallback to local authentication
                    return NeonAuth._authenticate_local_user(email, password)
                    
            except Exception as e:
                current_app.logger.error(f"Neon Auth error: {str(e)}")
                # Fallback to local authentication
                return NeonAuth._authenticate_local_user(email, password)
        else:
            # Use local authentication
            return NeonAuth._authenticate_local_user(email, password)
    
    @staticmethod
    def _authenticate_local_user(email, password):
        """Authenticate user with local credentials"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def send_password_reset(email):
        """
        Send password reset using Neon Auth or alternative method
        
        Args:
            email: User email
        
        Returns:
            bool: Success status
        """
        # If Neon Auth is enabled, use their password reset functionality
        if current_app.config.get('NEON_AUTH_ENABLED'):
            try:
                # This is a hypothetical implementation
                response = requests.post(
                    f"{current_app.config['NEON_AUTH_URL']}/recover",
                    headers={
                        "Authorization": f"Bearer {current_app.config['NEON_API_KEY']}",
                        "Content-Type": "application/json"
                    },
                    json={"email": email}
                )
                
                return response.status_code == 200
            except Exception as e:
                current_app.logger.error(f"Neon Auth password reset error: {str(e)}")
                return False
        else:
            # Implement local password reset logic (without email)
            # For a production app, you would integrate with a proper email service
            # For now, we'll just return True as a placeholder
            return True
    
    @staticmethod
    def verify_password_reset_token(token):
        """
        Verify password reset token
        
        Args:
            token: Password reset token
        
        Returns:
            dict: Token payload if valid, None otherwise
        """
        try:
            # Verify JWT token
            payload = jwt.decode(
                token, 
                current_app.config['JWT_SECRET_KEY'], 
                algorithms=['HS256']
            )
            return payload
        except jwt.InvalidTokenError:
            return None