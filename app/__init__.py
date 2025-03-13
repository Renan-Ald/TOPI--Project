from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(app)
    JWTManager(app)
    
    from app.routes import routes
    app.register_blueprint(routes)

    return app