#!/usr/bin/env python3
import os
import sys
sys.path.append('server')

# Set environment variables for local development
os.environ['DATABASE_URL'] = 'sqlite:///instance/soko_safi.db'
os.environ['SECRET_KEY'] = 'dev-secret-key'
os.environ['FLASK_ENV'] = 'development'
os.environ['DEBUG'] = 'True'
os.environ['CLOUDINARY_CLOUD_NAME'] = 'dqmvnmzqg'
os.environ['CLOUDINARY_UPLOAD_PRESET'] = 'soko_safi'

try:
    from server.app import create_app
    from server.app.extensions import db
    
    app = create_app()
    
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
    
    print("Starting server on http://127.0.0.1:5001")
    app.run(host='127.0.0.1', port=5001, debug=True)
    
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()