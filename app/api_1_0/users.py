from . import api
from flask import jsonify, request, abort
from flasgger import swag_from
from app.models.users import *
from sqlalchemy import exc
from flask_httpauth import HTTPBasicAuth

# 用户登陆
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    user_data = User.query.filter_by(UserName=str(username)).first_or_404()
    if user_data:
        return user_data.Password
    return None


@auth.hash_password
def hash_pw(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()


@auth.error_handler
def error_handler():
    abort(401)


@api.route('/user', methods=['GET'])
@auth.login_required
@swag_from('api_specs_yml/user/user.yml')
def user():
    """
    查询用户信息
    """
    user_data = User.query.filter_by(UserName=auth.username()).first_or_404().to_json()
    return jsonify(user_data)


@api.route('/user', methods=['POST'])
@swag_from('api_specs_yml/user/register.yml')
def register():
    """
    用户注册
    """
    # 尝试添加用户
    try:
        new_user = User.from_json(request.json)
        db.session.add(new_user)
        db.session.commit()
    except exc.SQLAlchemyError:
        # 发生错误，回滚
        db.session.rollback()
        return jsonify({"error": "User add failed."})

    user_data = User.query.filter_by(UserName=request.json['userName']).first_or_404().to_json()
    return jsonify(user_data)


@api.route('/user/reset_password', methods=['POST'])
@swag_from('api_specs_yml/user/reset_password.yml')
def reset_password():
    """
    密码重置
    """
    data = User.reset_password(email=request.json['email'], username=request.json['userName'])
    return jsonify(data)


@api.route('/user/project_follow_list', methods=['POST'])
@auth.login_required
@swag_from('api_specs_yml/user/follow_list_add.yml')
def follow_list_add():
    """
    添加项目到关注列表
    """
    user = User.query.filter_by(UserName=auth.username()).first_or_404()
    result = user.add_follow_project(project_id=request.json['project_id'])
    data = {
        'message': result
    }
    return jsonify(data)


@api.route('/user/project_follow_list', methods=['DELETE'])
@auth.login_required
@swag_from('api_specs_yml/user/follow_list_delete.yml')
def follow_list_delete():
    """
    从关注列表删除项目
    """
    user = User.query.filter_by(UserName=auth.username()).first_or_404()
    result = user.del_follow_project(project_id=request.json['project_id'])
    data = {
        'message': result
    }
    return jsonify(data)


@api.route('/user/project_follow_list', methods=['GET'])
@auth.login_required
@swag_from('api_specs_yml/user/follow_list.yml')
def follow_list():
    """
    关注列表
    """

    if 'CurrentPage' in request.args:
        current_page = int(request.args['CurrentPage'])
    else:
        current_page = 1
    if 'ItemsPerPage' in request.args:
        items_per_page = int(request.args['ItemsPerPage'])
    else:
        items_per_page = 10
    project = User.query.filter_by(UserName=auth.username()).first_or_404().get_follow_list(
        current_page=current_page, items_per_page=items_per_page)
    data = {
        "Page": {
            "PageCount": project[0],
            "CurrentPage": project[1],
            "ItemsPerPage": project[2],
        },
        "Project": project[3]
    }
    return jsonify(data)


@api.route('/user/subscriptions', methods=['GET'])
@auth.login_required
@swag_from('api_specs_yml/user/subscriptions.yml')
def subscriptions():
    """
    订阅信息
    """
    if 'subs_filter' in request.args:
        data = {
            'message': request.args['subs_filter']
        }
        return jsonify(data)
    else:
        data = {
            'message': '订阅信息添加成功/订阅信息错误'
        }
        return jsonify(data)
