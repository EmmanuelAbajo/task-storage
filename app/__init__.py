from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config


db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    jwt.init_app(app)

    from models.tokens import TokenBlacklist

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(token):
        jti = token['jti']
        return TokenBlacklist.isJtiBlacklisted(jti)

    from .apiv1 import bp as apiv1_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(apiv1_blueprint,url_prefix='/api/v1')
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    
    return app
