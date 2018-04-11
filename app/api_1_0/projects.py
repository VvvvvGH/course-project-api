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


@api.route('/project/onbid/<string:project_id>')
@swag_from('api_specs_yml/project_onbid.yml')
def onbid(project_id):
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


@api.route('/project/corrected/<string:project_id>')
@swag_from('api_specs_yml/project_corrected.yml')
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


@api.route('/project/ended/<string:project_id>')
@swag_from('api_specs_yml/project_ended.yml')
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


@api.route('/project')
@swag_from('api_specs_yml/project.yml')
def project_basic_info():
    # TODO: Get data from MySQL
    """
    项目各城市统计信息
    城市分类链接
    """
    data = {

        "ProjectStatistics": {
            "TotalNumber": 65444,
            "Onbid": 54441,
            "Corrected": 564,
            "Ended": 4547,
        },
        "Cities": [
            {
                "City": "GZ",
                "URL": "/project/cities/GZ",
                "TotalNumber": 544,
                "Onbid": 556,
                "Corrected": 466,
                "Ended": 4666,
            },
            {
                "City": "FS",
                "URL": "/project/cities/FS",
                "TotalNumber": 5435,
                "Onbid": 53545,
                "Corrected": 35256,
                "Ended": 4626,
            },

        ]
    }
    return jsonify(data)


@api.route('/project/cities/<string:city>')
def city(city):
    # TODO: Get data from MySQL
    """
    项目列表分类
    """
    data = {
        "Page": {
            "PageCount": 100,
            "CurrentPage": 1,
            "ProjectPerPage": 10,
        },
        "ProjectList": [
            {
                "ProjID": "DDSDDSDS",
                "URL": "/project/" + "onbid/" + "<ProjID>"

            }
        ]
    }
    return jsonify(data)
