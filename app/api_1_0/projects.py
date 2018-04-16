from . import api
from flask import jsonify
from flasgger import swag_from


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


@api.route('/project/procurement_notices/<string:project_id>', methods=['GET'])
@swag_from('api_specs_yml/project/project_procurement_notices.yml')
def procurement_notices(project_id):
    # TODO: Get data from MySQL
    """
    正在进行的项目
    """
    data = {
        "ProjID": project_id,
        "ProjTitle": "",
        "City": "",
        "ProjBud": "",
        "PurQuantity": "",
        "ProjReq": "",
        "SupplierQuals": "",
        "DDL": "",
        "Addr": "",
        "BidStartTime": "",
        "BidStartAddr": "",
        "BidBond": "",
        "AnnounceDDL": "",
        "Publisher": "",
        "PubDate": "",
        "Attachment": "",
    }
    return jsonify(data)


@api.route('/project/correction_notice/<string:project_id>', methods=['GET'])
@swag_from('api_specs_yml/project/project_correction_notice.yml')
def corrected(project_id):
    # TODO: Get data from MySQL
    """
    项目更正信息
    """
    data = {
        "ProjID": project_id,
        "Content": "更正事项与内容",
    }
    return jsonify(data)


@api.route('/project/bid_notice/<string:project_id>', methods=['GET'])
@swag_from('api_specs_yml/project/project_bid_notice.yml')
def ended(project_id):
    # TODO: Get data from MySQL
    """
    已经结束的项目
    """
    data = {
        "ProjID": project_id,
        "ProjTitle": "",
        "ProjBud": "",
        "PurMethod": "",
        "SBs": "",
        "QuoteDetail": "",
        "ServiceReq": "",
        "Quantity": "",
        "Currency": "",
        "UnitPrice": "",
        "FinalPrice": "",
        "ReviewDate": "",
        "ReviewAddr": "",
        "ReviewCommittee": "",
        "Manager": "",
        "ReviewComment": "",
        "AnnounceDDL": "",
        "Attachment": "",
    }
    return jsonify(data)


@api.route('/project', methods=['GET'])
@swag_from('api_specs_yml//project/project.yml')
def project_basic_info():
    # TODO: Get data from MySQL
    """
    项目各城市统计信息
    城市分类链接
    """
    data = {

        "ProjectStatistics": {
            "TotalNumber": 65444,
            "procurement_notices": 54441,
            "correction_notice": 564,
            "bid_notice": 4547,
        },
        "Cities": [
            {
                "City": "GZ",
                "URL": "/project/cities/GZ",
                "TotalNumber": 544,
                "procurement_notices": 54441,
                "correction_notice": 564,
                "bid_notice": 4547,
            },
            {
                "City": "FS",
                "URL": "/project/cities/FS",
                "TotalNumber": 5435,
                "procurement_notices": 54441,
                "correction_notice": 564,
                "bid_notice": 4547,
            },

        ]
    }
    return jsonify(data)


@api.route('/project/cities', methods=['GET'])
@swag_from('api_specs_yml/project/cities.yml')
def city_list():
    # TODO: Get data from MySQL
    """
    城市列表
    """
    data = {
        "Page": {
            "PageCount": 100,
            "CurrentPage": 1,
            "ItemsPerPage": 10,
        },
        "Cities":
            {
                "GZ": "/api/1.0/project/cities/GZ",
                "FS": "/api/1.0/project/cities/FS"
            }
    }
    return jsonify(data)


@api.route('/project/cities/<string:city>', methods=['GET'])
@swag_from('api_specs_yml/project/project_city.yml')
def city(city):
    # TODO: Get data from MySQL
    """
    城市下的项目列表
    """
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
