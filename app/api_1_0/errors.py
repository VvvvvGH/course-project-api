from . import api
from app.exceptions import *
from flask import jsonify, request, render_template


@api.app_errorhandler(404)
def error_404(e):
    """
    Error handler 404
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify(
            {
                'Error': str(e),
            }
        )
        return response, 404
    else:
        return render_template('errors.html', error_msg=e, error_code=404), 404


@api.app_errorhandler(400)
def error_400(e):
    """
       Error handler 400
       Bad request
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify(
            {
                'Error': str(e),
            }
        )
        return response, 400
    else:
        return render_template('errors.html', error_msg=e, error_code=400), 400


@api.app_errorhandler(401)
def error_401(e):
    """
       Error handler 401
       Unauthorized
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify(
            {
                'Error': str(e),
            }
        )
        return response, 401
    else:
        return render_template('errors.html', error_msg=e, error_code=401), 401


@api.app_errorhandler(403)
def error_403(e):
    """
       Error handler 403
       Forbidden
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify(
            {
                'Error': str(e),
            }
        )
        return response, 403
    else:
        return render_template('errors.html', error_msg=e, error_code=403), 403


@api.app_errorhandler(405)
def error_405(e):
    """
       Error handler 405
       Method not allowed
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify(
            {
                'Error': str(e),
            }
        )
        return response, 405
    else:
        return render_template('errors.html', error_msg=e, error_code=405), 405


@api.app_errorhandler(500)
def error_405(e):
    """
       Error handler 500
       Internal server error
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify(
            {
                'Error': str(e),
            }
        )
        return response, 500
    else:
        return render_template('errors.html', error_msg=e, error_code=500), 500


@api.app_errorhandler(ValidationError)
def validation_error(e):
    return error_400(e)
