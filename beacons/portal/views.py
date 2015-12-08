from flask import Blueprint

portal = Blueprint('portal', __name__)


@portal.route('/')
@portal.route('/index')
@portal.route('/home')
def home():
    """
    Render Home Page
    """
    return "HELLO WORLD"
