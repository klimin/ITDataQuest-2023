from flask import render_template, g, jsonify, request
from config import conf
import time
from . import general


@general.context_processor
def inject_conf_general():
    return dict(conf=conf)

# Custom errors handling
@general.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response

    return render_template('404.html', exception=e, conf=conf, str=str), 404


@general.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', exception=e, conf=conf, str=str), 500


@general.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html', exception=e, conf=conf, str=str), 403
