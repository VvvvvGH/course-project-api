from . import api
from flask import jsonify, request
from flasgger import swag_from
from .project_models import *


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
    # TODO: Get data from MySQL
    """
    项目各城市统计信息
    城市分类链接
    """
    data = CityStatics().to_json()
    return jsonify(data)


@api.route('/project/cities', methods=['GET'])
@swag_from('api_specs_yml/project/cities.yml')
def city_list():
    # TODO: Get data from MySQL
    """
    城市列表
    """
    data = {"Cities": []}
    city_list = ['GD', 'GZ', 'SZ', 'ZH', 'ST', 'SG', 'FS', 'JM', 'ZJ', 'MM', 'HZ', 'MZ', 'SW', 'HY', 'YZ', 'QY',
                 'DG', 'ZS', 'JY', 'YF', 'SD']
    for city in city_list:
        data['Cities'].append(city)
    return jsonify(data)


@api.route('/project/cities/<string:city>', methods=['GET'])
@swag_from('api_specs_yml/project/project_city.yml')
def city(city):
    # TODO: Get data from MySQL
    """
    城市下的项目列表
    """
    # FIXME: Fix this list
    data = {
        "Page": {
            "PageCount": 100,
            "CurrentPage": 1,
            "ItemsPerPage": 10,
        },
        "Project": [
            {
                "ProjID": "adsa",
                "ProjTitle": "项目名称",
                "City": city,
                "PubDate": "2018-4-21",
                "DDL": "2018-4-25",
                "Type": "{procurement_notices, correction_notice, bid_notice}"
            }
        ]
    }
    return jsonify(data)


@api.route('/project/project_list', methods=['GET'])
@swag_from('api_specs_yml/project/project_list.yml')
def project_list():
    # TODO: Get data from MySQL
    """
    项目列表
    """

    if 'CurrentPage' in request.args:
        current_page = int(request.args['CurrentPage'])
    else:
        current_page = 1
    if 'ItemsPerPage' in request.args:
        items_per_page = int(request.args['ItemsPerPage'])
    else:
        items_per_page = 10

    project_type = request.args['ProjectType']
    data = ProjectList(current_page=current_page, items_per_page=items_per_page,
                       project_type=project_type).to_json()
    return jsonify(data)
