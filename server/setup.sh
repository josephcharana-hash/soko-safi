#!/bin/bash

echo "Setting up Soko Safi WebSocket Backend..."

# Install Python dependencies
pip install --break-system-packages -r requirements.txt

echo "Dependencies installed successfully!"
echo "Run the server with: python3 app.py"
echo "Test WebSocket with: open test_client.html in browser"
echo "Server will run on: http://localhost:5000"