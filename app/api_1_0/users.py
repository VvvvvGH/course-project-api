from . import api
from flask import jsonify, request
from flasgger import swag_from
from app.models.users import *
from sqlalchemy import exc


@api.route('/user', methods=['GET'])
@swag_from('api_specs_yml/user/user.yml')
def user():
    """
    查询用户信息
    """
    user_data = User.query.filter_by(UserName="Idiots").first_or_404().to_json()
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
@swag_from('api_specs_yml/user/follow_list_add.yml')
def follow_list_add():
    """
    添加项目到关注列表
    """
    user = User.query.filter_by(UUID="1c64ba58-455b-11e8-bf9c-00dbdfbc5c37").first_or_404()
    result = user.add_follow_project(project_id=request.json['project_id'])
    data = {
        'message': '项目添加成功/项目ID不存在'
    }
    return jsonify(data)


@api.route('/user/project_follow_list', methods=['GET'])
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
    project = User.query.filter_by(UUID="14defa08-510b-11e8-ae6e-00dbdfbc5c37").first_or_404().get_follow_list(
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


@api.route('/user/project_follow_list', methods=['DELETE'])
@swag_from('api_specs_yml/user/follow_list_delete.yml')
def follow_list_delete():
    """
    从关注列表删除项目
    """
    data = {
        'message': '项目删除成功/项目ID不存在'
    }
    return jsonify(data)


@api.route('/user/subscriptions', methods=['GET'])
@swag_from('api_specs_yml/user/subscriptions.yml')
def subscriptions():
    """
    订阅过滤信息
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
