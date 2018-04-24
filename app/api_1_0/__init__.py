from flask import Blueprint

api = Blueprint('api', __name__)

# 在main后引入，　避免循环引入依赖
from . import projects
from . import users
from . import errors
from . import authentication
from . import decorators
from . import project_models
