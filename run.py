#!/usr/bin/env python
"""
Author: Rajat Gupta
"""

from beacons import app
import uuid
import logging
from logging import FileHandler, Formatter


if __name__ == '__main__':
    app.config['LOG_FILE'] = 'application.log'

    file_handler = FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True)
