#!/usr/bin/env python
"""
Author: Rajat Gupta
"""

from beacons import app
import uuid
import logging
import logging.config
import yaml


if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())

    logging.config.dictConfig(yaml.load(open('logging.conf')))

    logfile = logging.getLogger('file')
    logconsole = logging.getLogger('console')
    logfile.debug("Debug FILE")
    logconsole.debug("Debug CONSOLE")

    app.run(debug=True)
