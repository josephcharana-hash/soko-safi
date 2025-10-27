#!/usr/bin/env python
"""Test if Flask server can start"""

print("Testing Flask server startup...")

try:
    print("1. Importing Flask...")
    from flask import Flask
    print("✅ Flask imported")
    
    print("2. Importing extensions...")
    from app.extensions import db, socketio, session
    print("✅ Extensions imported")
    
    print("3. Creating app...")
    from app import create_app
    app = create_app()
    print("✅ App created")
    
    print("4. Testing database...")
    with app.app_context():
        db.create_all()
    print("✅ Database initialized")
    
    print("\n✅ All checks passed! Server should start successfully.")
    print("\nRun: python main.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nType: {type(e).__name__}")
    import traceback
    traceback.print_exc()
