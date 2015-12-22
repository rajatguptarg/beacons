from flask import Flask
from beacons.portal.view import portal


app = Flask(__name__)

app.config['LOG_FILE'] = 'application.log'

import logging
from logging import FileHandler, Formatter
file_handler = FileHandler(app.config['LOG_FILE'])
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'))

app.register_blueprint(portal)
