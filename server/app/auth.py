"""
Authentication utilities for Soko Safi
Handles password hashing, verification, and session management
"""

import bcrypt
from functools import wraps
from flask import session, request, jsonify, current_app
from app.models import User, UserRole

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        password (str): Plain text password
        hashed (str): Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login_user(user_id: str, role: str) -> None:
    """
    Create a user session
    
    Args:
        user_id (str): User's unique identifier
        role (str): User's role (buyer, artisan, admin)
    """
    session['user_id'] = user_id
    session['user_role'] = role
    session['authenticated'] = True

def logout_user() -> None:
    """
    Clear user session
    """
    session.clear()

def get_current_user() -> dict:
    """
    Get current authenticated user info
    
    Returns:
        dict: User info if authenticated, None otherwise
    """
    if session.get('authenticated'):
        return {
            'user_id': session.get('user_id'),
            'user_role': session.get('user_role')
        }
    return None

def require_auth(f):
    """
    Decorator to require authentication for routes
    
    Usage:
        @require_auth
        def protected_route():
            return "This is protected"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please log in to access this resource'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def require_role(*allowed_roles):
    """
    Decorator to require specific roles for routes
    
    Args:
        *allowed_roles: List of allowed roles (buyer, artisan, admin)
        
    Usage:
        @require_role('admin', 'artisan')
        def admin_or_artisan_route():
            return "This requires admin or artisan role"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('authenticated'):
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Please log in to access this resource'
                }), 401
            
            user_role = session.get('user_role')
            if user_role not in allowed_roles:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'This resource requires one of: {", ".join(allowed_roles)}'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_ownership_or_role(resource_user_id_param='user_id', *allowed_roles):
    """
    Decorator to require either ownership of resource or specific roles
    
    Args:
        resource_user_id_param (str): Parameter name containing the resource owner's user_id
        *allowed_roles: List of allowed roles that can access any resource
        
    Usage:
        @require_ownership_or_role('user_id', 'admin')
        def user_profile(user_id):
            return "User can access own profile, admin can access any"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('authenticated'):
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Please log in to access this resource'
                }), 401
            
            current_user_id = session.get('user_id')
            user_role = session.get('user_role')
            
            # Check if user has required role
            if user_role in allowed_roles:
                return f(*args, **kwargs)
            
            # Check if user owns the resource
            resource_user_id = kwargs.get(resource_user_id_param)
            if current_user_id == resource_user_id:
                return f(*args, **kwargs)
            
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only access your own resources'
            }), 403
            
        return decorated_function
    return decorator
