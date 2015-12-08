from flask import Blueprint, render_template

portal = Blueprint('portal', __name__)


@portal.route('/')
@portal.route('/index')
@portal.route('/home')
def home():
    """
    Render Home Page
    """
    return render_template('index.jinja')
