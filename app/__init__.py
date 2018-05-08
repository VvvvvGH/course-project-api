from flask import Flask
from config import config
from flasgger import Swagger
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

db = SQLAlchemy(use_native_unicode='utf8')
mail = Mail()
swagger = Swagger()


def create_app(config_name):
    # 初始化
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 注册API Blueprint
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/1.0')

    # Swagger
    swagger.init_app(app)

    # 注册Main
    from .main import main as main_route
    app.register_blueprint(main_route, url_prefix='/')


    # 数据库
    db.init_app(app)

    # Email
    mail.init_app(app)

    # ProxyFix
    # 修复使用nginx 反向代理启用https产生的问题
    # 需在nginx配置文件内添加以下内容
    # proxy_set_header   Host $host;
    # proxy_set_header   X-Forwarded-Proto  $scheme;
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
