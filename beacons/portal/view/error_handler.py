"""
Author: Rajat Gupta
"""
from flask import render_template
from beacons.portal.view import portal
import beacons


@portal.app_errorhandler(404)
def page_not_found(e):
    """
    Handle 404 Errors
    """
    beacons.app.logger.error('404 Occured. Explanation: ' + str(e))
    return render_template('404.jinja'), 404


@portal.app_errorhandler(403)
def forbidden(e):
    """
    Handle 403 Errors
    """
    beacons.app.logger.error('403 Occured. Explanation: ' + str(e))
    return render_template('403.jinja'), 403


@portal.app_errorhandler(410)
def gone(e):
    """
    Handle 410 Errors
    """
    beacons.app.logger.error('410 Occured. Explanation: ' + str(e))
    return render_template('410.jinja'), 410


@portal.app_errorhandler(405)
def method_not_allowed(e):
    """
    Handle 405 Errors
    """
    beacons.app.logger.error('405 Occured. Explanation: ' + str(e))
    return render_template('405.jinja'), 405


@portal.app_errorhandler(500)
def internal_server_error(e):
    """
    Handle 500 Errors
    """
    beacons.app.logger.error('500 Occured. Explanation: ' + str(e))
    return render_template('500.jinja'), 500


@portal.app_errorhandler(Exception)
def exceptions(e):
    """
    Handle All Exceptions
    """
    beacons.app.logger.error('Exception Occured. Explanation: ' + str(e))
    return render_template('exception.jinja', exception=e)
