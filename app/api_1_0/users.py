from . import api
from flask import jsonify, request
from flasgger import swag_from


@api.route('/user', methods=['GET'])
@swag_from('api_specs_yml/user/user.yml')
def user():
    """
    查询用户信息
    """
    data = {
        "activated": True,
        "last_login": "24 Mar 2018 15:51:25",
        "login_state": True,
        "subscriptions": "/user/focus",
        "username": "Cheng",
        "uuid": "2b232156-3bbe-4e5d-a379-9e59b8e7b81a"
    }
    return jsonify(data)


@api.route('/user', methods=['POST'])
@swag_from('api_specs_yml/user/register.yml')
def register():
    """
    用户注册
    """
    data = {
        "activated": False,
        "last_login": "24 Mar 2018 15:51:25",
        "login_state": False,
        "subscriptions": "/user/subs",
        "username": "Cheng",
        "uuid": "2b232156-3bbe-4e5d-a379-9e59b8e7b81a"
    }
    return jsonify(data)


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
    data = {
        "Page": {
            "PageCount": 100,
            "CurrentPage": 1,
            "ItemsPerPage": 10,
        },
        "Project": [
            {
                "ProjID": "项目ID",
                "ProjTitle": "项目名称",
                "City": "city",
                "PubDate": "2018-4-21",
                "DDL": "2018-4-25",
                "Type": "{procurement_notices, correction_notice, bid_notice}",
                "URL": "/project/bid_notice/FS4456444"
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
