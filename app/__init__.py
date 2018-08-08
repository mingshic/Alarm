from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .model.settings import Mysqlconfig


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(Mysqlconfig)
    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)    

    return app
