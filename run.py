#!/usr/bin/env python
"""
Author: Rajat Gupta
"""

import uuid
import logging
from logging import FileHandler, Formatter
from beacons import app


if __name__ == '__main__':
    app.config['LOG_FILE'] = 'application.log'

    FILE_HANDLER = FileHandler(app.config['LOG_FILE'])
    FILE_HANDLER.setLevel(logging.INFO)
    app.logger.addHandler(FILE_HANDLER)

    FILE_HANDLER.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True)
