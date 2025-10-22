from flask import Flask
from models import db
from routes import register_blueprints

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soko_safi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
register_blueprints(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)