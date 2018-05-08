from flask_httpauth import HTTPBasicAuth
from flask import abort, jsonify
from . import api
from ..exceptions import UserNotActivatedError
from app.models.users import User
import hashlib
import base64
import re

# 用户登陆
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    user = User.query.filter_by(UserName=str(username)).first_or_404()
    # Hack to force user to activate
    if not user.UserBackground[0].Activated:
        raise UserNotActivatedError("User not activated!")
    if user:
        return user.Password
    return None


@auth.hash_password
def hash_pw(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()


@auth.error_handler
def error_handler():
    abort(401)


@api.route('user/activate/<activate_token>', methods=['GET'])
def activate(activate_token):
    token = re.findall("b\'([A-z\d]+)\'([a-z\d]+)", activate_token)[0]
    user = User.query.filter_by(UUID=base64.b64decode(token[0]).decode('utf-8')).first()
    if user and hashlib.md5(user.Password.encode('utf-8')).hexdigest() == token[1] and user.UserBackground[
        0].Activated == 0:
        user.UserBackground[0].Activated = 1
        return jsonify({"message": "激活成功，用户已激活"})
    return jsonify({"message": "激活失败"})
