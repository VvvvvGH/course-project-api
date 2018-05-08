from . import api
from flask import jsonify, request
from flasgger import swag_from
from app.models.project import *


@api.route('/')
def index():
    """
    Index
    ---
    responses:
      200:
        description: Return the resources
        schema:
            type: object
            properties:
                message:
                    type: string
                    example: "Please read the doc to use API"
       """
    return jsonify({
        "message": "Please read the doc to use API"
    })


@api.route('/project/procurement_notices/<string:ProjectID>', methods=['GET'])
@swag_from('api_specs_yml/project/project_procurement_notices.yml')
def project_ongoing(ProjectID):
    """
    正在进行的项目
    """

    data = ProjectOngoing.query.filter_by(ProjID=str(ProjectID)).first_or_404().to_json()

    return jsonify(data)


@api.route('/project/correction_notice/<string:ProjectID>', methods=['GET'])
@swag_from('api_specs_yml/project/project_correction_notice.yml')
def project_corrected(ProjectID):
    """
    项目更正信息
    """
    data = ProjectCorrected.query.filter_by(ProjID=str(ProjectID)).first_or_404().to_json()

    return jsonify(data)


@api.route('/project/bid_notice/<string:ProjectID>', methods=['GET'])
@swag_from('api_specs_yml/project/project_bid_notice.yml')
def project_ended(ProjectID):
    """
    已经结束的项目
    """
    data = ProjectEnded.query.filter_by(ProjID=str(ProjectID)).first_or_404().to_json()

    return jsonify(data)


@api.route('/project', methods=['GET'])
@swag_from('api_specs_yml/project/project.yml')
def project_basic_info():
    """
    项目各城市统计信息
    城市分类链接
    """
    data = CityStatics().to_json()
    return jsonify(data)


@api.route('/project/cities', methods=['GET'])
@swag_from('api_specs_yml/project/cities.yml')
def city_list():
    """
    城市列表
    """
    data = {"Cities": []}
    city_list = ['GD', 'GZ', 'SZ', 'ZH', 'ST', 'SG', 'FS', 'JM', 'ZJ', 'MM', 'HZ', 'MZ', 'SW', 'HY', 'YZ', 'QY',
                 'DG', 'ZS', 'JY', 'YF', 'SD']
    for city in city_list:
        data['Cities'].append(city)
    return jsonify(data)


@api.route('/project/project_list', methods=['GET'])
@swag_from('api_specs_yml/project/project_list.yml')
def project_list():
    """
    项目列表
    """

    city_list = ['GD', 'GZ', 'SZ', 'ZH', 'ST', 'SG', 'FS', 'JM', 'ZJ', 'MM', 'HZ', 'MZ', 'SW', 'HY', 'YZ', 'QY',
                 'DG', 'ZS', 'JY', 'YF', 'SD']

    if 'CurrentPage' in request.args:
        current_page = int(request.args['CurrentPage'])
    else:
        current_page = 1
    if 'ItemsPerPage' in request.args:
        items_per_page = int(request.args['ItemsPerPage'])
    else:
        items_per_page = 10
    project_type = request.args['ProjectType']
    city = None
    search_token = None
    if 'City' in request.args and request.args['City'].upper() in city_list:
        city = request.args['City'].upper()
    if 'SearchToken' in request.args:
        search_token = request.args['SearchToken']
        # 　若用户已登录　添加搜索记录
        if auth.username():
            user = User.query.filter_by(UserName=auth.username()).first()
            if user:
                user.add_search_record(search_token)

    data = ProjectList(current_page=current_page, items_per_page=items_per_page,
                       project_type=project_type, city=city, search_token=search_token).to_json()
    return jsonify(data)
