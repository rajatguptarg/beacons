"""
Author: Rajat Gupta
"""

from flask import render_template
from beacons.portal.view import portal


@portal.app_errorhandler(404)
def page_not_found(e):
    """
    Handle 404 Errors
    """
    return render_template('404.jinja'), 404


@portal.app_errorhandler(403)
def forbidden(e):
    """
    Handle 403 Errors
    """
    return render_template('403.jinja'), 403


@portal.app_errorhandler(410)
def gone(e):
    """
    Handle 410 Errors
    """
    return render_template('410.jinja'), 410


@portal.app_errorhandler(500)
def internal_server_error(e):
    """
    Handle 500 Errors
    """
    return render_template('500.jinja'), 500


@portal.app_errorhandler(Exception)
def exceptions(e):
    """
    Handle All Exceptions
    """
    return render_template('exception.jinja', exception=e)
