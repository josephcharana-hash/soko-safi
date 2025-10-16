from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    from .routes.user_routes import user_bp
    from .routes.product_routes import product_bp

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(product_bp, url_prefix="/products")

    return app
