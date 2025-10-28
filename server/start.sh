#!/bin/bash

echo "🚀 Starting Soko Safi Backend..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cat > .env << EOF
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///soko_safi.db
FLASK_ENV=development
EOF
    echo "✅ .env file created"
fi

# Check Python version
echo "🐍 Python version:"
python --version

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q flask flask-cors flask-sqlalchemy flask-session flask-socketio python-dotenv bcrypt

# Start server
echo "🔥 Starting Flask server on port 5001..."
python main.py
