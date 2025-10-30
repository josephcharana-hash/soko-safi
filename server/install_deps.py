#!/usr/bin/env python3
import subprocess
import sys

packages = [
    'flask',
    'flask-restful', 
    'flask-sqlalchemy',
    'flask-socketio',
    'flask-session',
    'flask-cors',
    'python-dotenv',
    'cloudinary',
    'alembic'
]

for package in packages:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"✓ Installed {package}")
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")