from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from routes.user_routes import user_bp
from routes.product_routes import product_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soko.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# register blueprints
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(product_bp, url_prefix='/products')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
