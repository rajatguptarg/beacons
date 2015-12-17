from flask import Blueprint
import flask


offer = Blueprint('offer', __name__)


@offer.route('/offers')
def get_offers():
    return 'Under Construction'