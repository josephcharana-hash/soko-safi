#!/usr/bin/env python3
import os
from main import app, socketio

if __name__ == '__main__':
    print("🚀 Starting Soko Safi Development Server...")
    print("📍 Server will be available at: http://localhost:5001")
    print("🔧 Debug mode: ON")
    
    # Run in development mode
    socketio.run(
        app, 
        debug=True, 
        host='0.0.0.0', 
        port=5001,
        allow_unsafe_werkzeug=True
    )