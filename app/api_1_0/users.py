from . import api
from flask import jsonify, request
from flasgger import swag_from
from app import db
from app.models import *
from .user_models import *
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
    data = {
        'message': '验证成功，密码重置链接已经发送到邮箱'
    }
    return jsonify(data)


@api.route('/user/project_follow_list', methods=['POST'])
@swag_from('api_specs_yml/user/follow_list_add.yml')
def follow_list_add():
    """
    添加项目到关注列表
    """
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

    project = UserFocus.query.filter_by(UUID="1c64ba58-455b-11e8-bf9c-00dbdfbc5c37").first_or_404()
    data = {
        "Page": {
            "PageCount": 1,
            "CurrentPage": 1,
            "ItemsPerPage": 10,
        },
        "Project": [
            {
                "ProjID": project.ProjID,
                "ProjTitle": "项目名称",
                "City": "city",
                "PubDate": "2018-4-21",
                "DDL": "2018-4-25",
                "Type": "{procurement_notices, correction_notice, bid_notice}",
                "URL": "/project/bid_notice/" + project.ProjID
            }
        ]
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
