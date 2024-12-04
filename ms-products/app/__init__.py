import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.Config import config
from app.Config.cache_config import cache_config
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cache = Cache()

def create_app() -> Flask:
    
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app, config=cache_config)
    CORS(app)

    # Register Blueprints
    from app.Routes.product import product
    app.register_blueprint(product)
    
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app
