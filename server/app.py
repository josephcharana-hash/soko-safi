from flask import Flask
from models import db
from routes import register_blueprints
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'

db.init_app(app)
register_blueprints(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    try:
        print("Starting Flask app with PostgreSQL...")
        app.run(debug=True, port=5001, host='0.0.0.0')
    except Exception as e:
        print(f"Error starting app: {e}")