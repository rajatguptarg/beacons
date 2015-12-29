from flask import Blueprint


portal = Blueprint('portal', __name__)


from beacons.portal.view import views, error_handler


__all__ = [portal, 'views', 'error_handler']
