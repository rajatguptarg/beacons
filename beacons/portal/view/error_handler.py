from flask import render_template
from beacons.portal.view import portal


@portal.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.jinja'), 404


@portal.app_errorhandler(403)
def forbidden(e):
    return render_template('403.jinja'), 403


@portal.errorhandler(410)
def gone(e):
    return render_template('410.jinja'), 410


@portal.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.jinja'), 500


@portal.errorhandler(Exception)
def exceptions(e):
    return render_template('exception.jinja', exception=e)
