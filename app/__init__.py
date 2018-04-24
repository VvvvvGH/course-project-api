from flask import Flask
from config import config
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

# TODO: Import Email
# TODO: SQLAlchemy

db = SQLAlchemy(use_native_unicode='utf8')


def create_app(config_name):
    # 初始化
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Swagger
    swagger = Swagger(app)

    # 注册API Blueprint
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/1.0')

    # 注册Main
    from .main import main as main_route
    app.register_blueprint(main_route, url_prefix='/')

    # 数据库
    db.init_app(app)

    return app
