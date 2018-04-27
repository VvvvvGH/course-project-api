from flask import Flask
from config import config
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
# TODO: Import Email
# TODO: SQLAlchemy

db = SQLAlchemy(use_native_unicode='utf8')


def create_app(config_name):
    # 初始化
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # ProxyFix
    # 修复使用nginx 反向代理启用https产生的问题
    # 需在nginx配置文件内添加以下内容
    # proxy_set_header   Host $host;
    # proxy_set_header   X-Forwarded-Proto  $scheme;
    app.wsgi_app = ProxyFix(app.wsgi_app)

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
