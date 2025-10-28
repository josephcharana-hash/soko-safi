"""
Script to create an admin user for Soko Safi
Run this script to create the first admin user
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User, UserRole
from app.auth import hash_password

load_dotenv()

def create_admin_user():
    """Create an admin user"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(role=UserRole.admin, deleted_at=None).first()
        if existing_admin:
            print(f"❌ Admin user already exists: {existing_admin.email}")
            return
        
        # Get admin details
        print("🔐 Creating Admin User for Soko Safi")
        print("=" * 40)
        
        email = input("Enter admin email: ").strip()
        if not email:
            print("❌ Email is required")
            return
        
        password = input("Enter admin password: ").strip()
        if not password:
            print("❌ Password is required")
            return
        
        full_name = input("Enter admin full name: ").strip()
        if not full_name:
            print("❌ Full name is required")
            return
        
        phone = input("Enter admin phone (optional): ").strip()
        location = input("Enter admin location (optional): ").strip()
        
        try:
            # Create admin user
            admin_user = User(
                email=email.lower(),
                password_hash=hash_password(password),
                full_name=full_name,
                role=UserRole.admin,
                phone=phone,
                location=location,
                is_verified=True
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            print(f"📧 Email: {admin_user.email}")
            print(f"👤 Name: {admin_user.full_name}")
            print(f"🔑 Role: {admin_user.role.value}")
            print(f"✅ Verified: {admin_user.is_verified}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin user: {str(e)}")

if __name__ == "__main__":
    create_admin_user()
