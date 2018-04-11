from flask import Blueprint

main = Blueprint('main', __name__)

# 在main后引入，　避免循环引入依赖
from . import views

