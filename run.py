#!/usr/bin/env python
"""
Author: Rajat Gupta
"""

import uuid
from beacons import app


if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True)
